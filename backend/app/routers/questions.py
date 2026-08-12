# backend/app/routers/questions.py
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.questions import Question, QuestionType
from app.schemas.questions import QuestionCreate, QuestionUpdate, QuestionDelete, QuestionResponse

router = APIRouter()

def get_current_uid(request: Request) -> str:
    uid = getattr(request.state, "uid", None)
    if not uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return uid

@router.post("/create", response_model=QuestionResponse)
async def create_question(
    request: Request, ques: QuestionCreate, db: AsyncSession = Depends(get_db)
):
    get_current_uid(request)
    if ques.question_type not in QuestionType:
        raise HTTPException(status_code=400, detail="Invalid question type")
    
    new_question = Question(
        quiz_id=ques.quiz_id,
        question=ques.question,
        question_type=ques.question_type,
        correct_answer=ques.correct_answer,
    )
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return new_question

@router.get("/update", response_model=QuestionResponse)
async def update_question(
    request: Request, ques: QuestionUpdate, db: AsyncSession = Depends(get_db)
):
    get_current_uid(request)
    result = await db.execute(select(Question).where(Question.id == ques.question_id))
    question_obj = result.scalar_one_or_none()
    
    if not question_obj:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question_obj.question = ques.question
    question_obj.question_type = ques.question_type
    question_obj.correct_answer = ques.correct_answer
    await db.commit()
    await db.refresh(question_obj)
    return question_obj

@router.delete("/delete")
async def delete_question(
    request: Request, ques: QuestionDelete, db: AsyncSession = Depends(get_db)
):
    get_current_uid(request)
    result = await db.execute(select(Question).where(Question.id == ques.question_id))
    question_obj = result.scalar_one_or_none()
    
    if not question_obj:
        raise HTTPException(status_code=404, detail="Question not found")
        
    await db.delete(question_obj)
    await db.commit()
    return {"message": "Question deleted successfully"}