# backend/app/routers/ingest.py
import os
import shutil
from pathlib import Path

from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.base import get_db
from app.models.quiz_resource import QuizResource

router = APIRouter(tags=["Ingestion"])

# Base upload directory (relative to backend root)
UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"


@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    quiz_id: int = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a file to local disk and record it in the DB.
    No parsing or embedding happens here — that's deferred to quiz generation.
    """
    uid = getattr(request.state, "uid", None)
    if not uid or not quiz_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")

    # Create quiz-specific upload directory
    quiz_upload_dir = UPLOAD_DIR / str(quiz_id)
    quiz_upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file to disk
    file_path = quiz_upload_dir / file.filename
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    finally:
        await file.close()

    file_size_mb = round(len(content) / (1024 * 1024), 2)

    # Record in DB
    resource = QuizResource(
        quiz_id=quiz_id,
        filename=file.filename,
        file_path=str(file_path),
        file_size_mb=file_size_mb,
    )
    db.add(resource)
    await db.commit()
    await db.refresh(resource)

    return {
        "status": "success",
        "resource_id": resource.id,
        "filename": resource.filename,
        "file_size_mb": resource.file_size_mb,
        "quiz_id": quiz_id,
    }


@router.get("/resources/{quiz_id}")
async def list_resources(
    quiz_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """List all uploaded resources for a quiz."""
    uid = getattr(request.state, "uid", None)
    if not uid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await db.execute(
        select(QuizResource).where(QuizResource.quiz_id == quiz_id)
    )
    resources = result.scalars().all()

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "file_size_mb": r.file_size_mb,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in resources
    ]


@router.delete("/resources/{quiz_id}/{resource_id}")
async def delete_resource(
    quiz_id: int,
    resource_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Delete a single uploaded resource (file + DB record)."""
    uid = getattr(request.state, "uid", None)
    if not uid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await db.execute(
        select(QuizResource).where(
            QuizResource.id == resource_id,
            QuizResource.quiz_id == quiz_id,
        )
    )
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Delete file from disk
    try:
        file_path = Path(resource.file_path)
        if file_path.exists():
            file_path.unlink()
    except Exception:
        pass  # File may already be gone

    await db.delete(resource)
    await db.commit()

    return {"status": "deleted", "resource_id": resource_id}


def cleanup_quiz_uploads(quiz_id: int):
    """Remove the entire uploads directory for a quiz. Called after publish."""
    quiz_upload_dir = UPLOAD_DIR / str(quiz_id)
    if quiz_upload_dir.exists():
        shutil.rmtree(quiz_upload_dir, ignore_errors=True)