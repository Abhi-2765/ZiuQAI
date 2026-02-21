from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.base import get_db
from ..models.user_responses import UserResponse
from ..models.questions import Question
from ..models.participants import Participant
from ..schemas.user_responses import UserResponseCreate, UserResponseUpdate, UserResponseDelete, UserResponseResponse

router = APIRouter()

@router.post("/create", response_model=UserResponseResponse)
async def create_user_response(request: Request, user_response: UserResponseCreate, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")
    
        participant_id, question_id, response = user_response.participant_id, user_response.question_id, user_response.response
        if not participant_id or not question_id or not response:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        participant = await db.execute(select(Participant).where(Participant.id == participant_id))
        if not participant.scalars().first():
            raise HTTPException(status_code=404, detail="Participant not found")
        
        question = await db.execute(select(Question).where(Question.id == question_id))
        if not question.scalars().first():
            raise HTTPException(status_code=404, detail="Question not found")
        
        new_user_response = UserResponse(
            participant_id=participant_id,
            qid=question_id,
            response=response,
        )

        db.add(new_user_response)
        await db.commit()
        await db.refresh(new_user_response)
        return new_user_response
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update", response_model=UserResponseResponse)
async def update_user_response(request: Request, user_response: UserResponseUpdate, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")
    
        user_response_id, response = user_response.user_response_id, user_response.response
        if not user_response_id or not response:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        user_response = await db.execute(select(UserResponse).where(UserResponse.id == user_response_id))
        if not user_response.scalars().first():
            raise HTTPException(status_code=404, detail="User response not found")
        
        user_response = db.query(UserResponse).filter(UserResponse.id == user_response_id).first()
        user_response.response = response
        
        await db.commit()
        await db.refresh(user_response)
        return user_response
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/delete", response_model=UserResponseResponse)
async def delete_user_response(request: Request, user_response: UserResponseDelete, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")
    
        user_response_id = user_response.user_response_id
        if not user_response_id:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        user_response = await db.execute(select(UserResponse).where(UserResponse.id == user_response_id))
        if not user_response.scalars().first():
            raise HTTPException(status_code=404, detail="User response not found")
        
        await db.delete(user_response)
        await db.commit()
        return user_response
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))