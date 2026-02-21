from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..schemas.participants import ParticipantCreate, ParticipantUpdate, ParticipantResponse, ParticipantDelete
from ..models.participants import Participant
from ..models.quizes import Quiz
from ..db.base import get_db

router = APIRouter()

@router.post("/create", response_model=ParticipantResponse)
async def create_participant(
    request: Request,
    participant: ParticipantCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        uid = request.state.uid

        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")

        new_participant = Participant(
            quiz_id=participant.quiz_id,
            user_id=uid,
        )

        db.add(new_participant)
        await db.commit()
        await db.refresh(new_participant)

        return new_participant

    except Exception as e:
        await db.rollback()
        print(f"Error creating participant: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete")
async def remove_participation(
    request: Request,
    participant: ParticipantDelete,
    db: AsyncSession = Depends(get_db)
):
    try:
        uid = request.state.uid

        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")

        db.execute(delete(Participant).where(Participant.quiz_id == participant.quiz_id, Participant.user_id == uid))
        await db.commit()

        return {"message": "Participation removed successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))