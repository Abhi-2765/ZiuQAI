from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.base import get_db
from ..models.user_responses import UserResponse
from ..models.quizes import Quiz
from ..models.questions import Question
from ..models.quiz_sessions import QuizSession
from ..schemas.user_responses import UserResponseCreate, UserResponseUpdate, UserResponseDelete, UserResponseResponse

router = APIRouter()

@router.post("/create", response_model=UserResponseResponse)
async def create_user_response(request: Request, user_response: UserResponseCreate, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")
    
        quiz_id, question_id, session_id, response = user_response.quiz_id, user_response.question_id, user_response.session_id, user_response.response
        if not quiz_id or not question_id or not session_id or not response:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        quiz = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
        if not quiz.scalars().first():
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        question = await db.execute(select(Question).where(Question.id == question_id))
        if not question.scalars().first():
            raise HTTPException(status_code=404, detail="Question not found")
        
        quiz_session = await db.execute(select(QuizSession).where(QuizSession.id == session_id))
        if not quiz_session.scalars().first():
            raise HTTPException(status_code=404, detail="Quiz session not found")
        
        new_user_response = UserResponse(
            uid=uid,
            quiz_id=quiz_id,
            qid=question_id,
            session_id=session_id,
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