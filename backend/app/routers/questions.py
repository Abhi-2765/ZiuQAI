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

@router.put("/update", response_model=QuestionResponse)
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
    if ques.options is not None:
        question_obj.options = ques.options
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

@router.get("/quiz/{quiz_id}")
async def get_quiz_questions(
    quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)
):
    get_current_uid(request)
    # The frontend owner will request this to see all questions for editing.
    # Note: Depending on rules, we might want to verify creator_uid = uid via the Quiz table, 
    # but since this is for owners we trust get_current_uid is enough for now, 
    # or we can join with Quiz.
    from app.models.quizes import Quiz
    uid = get_current_uid(request)
    result = await db.execute(
        select(Quiz).where(Quiz.id == quiz_id, Quiz.creator_uid == uid)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not authorized to view questions for this quiz")
        
    q_result = await db.execute(select(Question).where(Question.quiz_id == quiz_id))
    questions = q_result.scalars().all()
    
    return [
        {
            "id": q.id,
            "question": q.question,
            "question_type": q.question_type.value,
            "correct_answer": q.correct_answer,
            "options": q.options
        }
        for q in questions
    ]