from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db.base import get_db
from ..models.quiz_sessions import QuizSession
from ..models.quizes import Quiz
from ..schemas.quiz_sessions import QuizSessionCreate, QuizSessionUpdate, QuizSessionDelete, QuizSessionResponse

router = APIRouter()

@router.post("/create", response_model=QuizSessionResponse)
async def create_quiz_session(request: Request, quiz_session: QuizSessionCreate, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        quiz_id, quiz_start_time, quiz_duration = quiz_session.quiz_id, quiz_session.quiz_start_time, quiz_session.quiz_duration
        if not quiz_id or not quiz_start_time or not quiz_duration:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        quiz = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
        if not quiz.scalars().first():
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        new_quiz_session = QuizSession(
            user_id=uid,
            quiz_id=quiz_id,
            quiz_start_time=quiz_start_time,
            quiz_duration=quiz_duration,
        )
        db.add(new_quiz_session)
        await db.commit()
        await db.refresh(new_quiz_session)
        return QuizSessionResponse(**new_quiz_session.__dict__)
    except Exception as e:
        db.rollback()
        return HTTPException(status_code=500, detail=str(e))

@router.put("/update", response_model=QuizSessionResponse)
async def update_quiz_session(request: Request, quiz_session: QuizSessionUpdate, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        session_id, quiz_start_time, quiz_duration = quiz_session.session_id, quiz_session.quiz_start_time, quiz_session.quiz_duration
        if not session_id or not quiz_start_time or not quiz_duration:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        quiz = await db.execute(select(Quiz).where(Quiz.id == session_id))
        if not quiz.scalars().first():
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        quiz_session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
        quiz_session.quiz_start_time = quiz_start_time
        quiz_session.quiz_duration = quiz_duration
        
        await db.commit()
        await db.refresh(quiz_session)
        return quiz_session
    except Exception as e:
        db.rollback()
        return HTTPException(status_code=500, detail=str(e))

@router.delete("/delete", response_model=QuizSessionResponse)
async def delete_quiz_session(request: Request, quiz_session: QuizSessionDelete, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        session_id = quiz_session.session_id
        if not session_id:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        quiz_session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
        if not quiz_session:
            raise HTTPException(status_code=404, detail="Quiz session not found")
        
        await db.delete(quiz_session)
        await db.commit()
        return quiz_session
    except Exception as e:
        db.rollback()
        return HTTPException(status_code=500, detail=str(e))