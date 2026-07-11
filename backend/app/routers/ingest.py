# backend/app/routers/ingest.py
from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db

from app.services.core.interfaces import (
    EmbeddingService,
    SplittingService,
    ParsingService
)

from app.services.core.factory import (
    get_embedding_service,
    get_splitting_service,
    get_parsing_service
)

from app.services.ingestion.ingest import IngestionService

router = APIRouter(tags=["Ingestion"])


def get_ingestion_service(
    splitter: SplittingService = Depends(get_splitting_service),
    embedder: EmbeddingService = Depends(get_embedding_service),
) -> IngestionService:
    return IngestionService(
        splitter=splitter,
        embedding_model=embedder
    )


@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    quiz_id: int = None,
    db: AsyncSession = Depends(get_db),

    parser: ParsingService = Depends(get_parsing_service),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
):
    """
    Upload → Parse → Chunk → Embed → Store (LangChain PGVector)
    """

    try:
        uid = getattr(request.state, "uid", None)
        if not uid or not quiz_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if not file.filename:
            raise HTTPException(status_code=400, detail="Invalid file")

        text = await parser.parse(file)

        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Empty document")

        document, chunk_count = await ingestion_service.ingest_document(
            text=text,
            title=file.filename,
            quiz_id=quiz_id,
            user_id=uid,
            db=db
        )

        return {
            "status": "success",
            "document_id": document.id,
            "chunks_created": chunk_count,
            "quiz_id": quiz_id
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        await file.close()