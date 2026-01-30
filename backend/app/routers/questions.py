from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db.base import get_db
from ..models.questions import Question, QuestionType
from ..models.quizes import Quiz
from ..schemas.questions import QuestionCreate, QuestionUpdate, QuestionDelete, QuestionResponse

router = APIRouter()

@router.post("/create", response_model=QuestionResponse)
async def create_question(request: Request, ques: QuestionCreate, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")

        quiz_id, question, question_type, correct_answer = ques.quiz_id, ques.question, ques.question_type, ques.correct_answer
        if not quiz_id or not question or not question_type or not correct_answer:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        quiz = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
        if not quiz.scalars().first():
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        if question_type not in QuestionType:
            raise HTTPException(status_code=400, detail="Invalid question type")

        new_question = Question(
            quiz_id=quiz_id,
            question=question,
            question_type=question_type,
            correct_answer=correct_answer,
        )

        db.add(new_question)
        await db.commit()
        await db.refresh(new_question)
        return new_question

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/update", response_model=QuestionResponse)
async def update_question(request: Request, ques: QuestionUpdate, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")

        question_id, question, question_type, correct_answer = ques.question_id, ques.question, ques.question_type, ques.correct_answer

        if not question_id or not question or not question_type or not correct_answer:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        question = await db.execute(select(Question).where(Question.id == question_id))
        if not question.scalars().first():
            raise HTTPException(status_code=404, detail="Question not found")
        
        if question_type not in QuestionType:
            raise HTTPException(status_code=400, detail="Invalid question type")

        question = db.query(Question).filter(Question.id == question_id).first()
        question.question = question
        question.question_type = question_type
        question.correct_answer = correct_answer

        await db.commit()
        await db.refresh(question)
        return question

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
async def delete_question(request: Request, ques: QuestionDelete, db: AsyncSession = Depends(get_db)):
    try:
        uid = request.state.uid
        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")

        question_id = ques.question_id
        if not question_id:
            raise HTTPException(status_code=400, detail="Something went wrong")
        
        question = await db.execute(select(Question).where(Question.id == question_id))
        if not question.scalars().first():
            raise HTTPException(status_code=404, detail="Question not found")

        await db.delete(question)
        await db.commit()
        return {"message": "Question deleted successfully"}
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))