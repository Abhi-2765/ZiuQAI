from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..schemas.quizes import QuizCreate, QuizUpdate, QuizResponse, QuizDelete
from ..models.quizes import Quiz
from ..db.base import get_db

router = APIRouter()

@router.post("/create", response_model=QuizResponse)
async def create_quiz(
    request: Request,
    quiz: QuizCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        uid = request.state.uid

        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")

        new_quiz = Quiz(
            quiz_name=quiz.quiz_name,
            question_count=quiz.question_count,
            quiz_difficulty=quiz.quiz_difficulty,
            quiz_start_time=quiz.quiz_start_time,
            quiz_duration=quiz.quiz_duration,
            show_leaderboard=quiz.show_leaderboard,
            creator_uid=uid,
        )

        db.add(new_quiz)
        await db.commit()
        await db.refresh(new_quiz)

        return new_quiz

    except Exception as e:
        await db.rollback()
        print(f"Error creating quiz: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update", response_model=QuizResponse)
async def update_quiz(
    request: Request,
    quiz: QuizUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        uid = request.state.uid

        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")

        result = await db.execute(
            select(Quiz).where(
                Quiz.id == quiz.quiz_id,
                Quiz.creator_uid == uid,
            )
        )

        old_quiz = result.scalar_one_or_none()

        if not old_quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        old_quiz.quiz_name = quiz.quiz_name
        old_quiz.question_count = quiz.question_count
        old_quiz.quiz_difficulty = quiz.quiz_difficulty
        old_quiz.quiz_start_time = quiz.quiz_start_time
        old_quiz.quiz_duration = quiz.quiz_duration
        old_quiz.show_leaderboard = quiz.show_leaderboard

        await db.commit()
        await db.refresh(old_quiz)

        return old_quiz

    except Exception as e:
        await db.rollback()
        print(f"Error updating quiz: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete")
async def delete_quiz(
    request: Request,
    quiz: QuizDelete,
    db: AsyncSession = Depends(get_db),
):
    try:
        uid = request.state.uid

        if not uid:
            raise HTTPException(status_code=401, detail="Unauthorized")

        result = await db.execute(
            select(Quiz).where(
                Quiz.id == quiz.quiz_id,
                Quiz.creator_uid == uid,
            )
        )
        old_quiz = result.scalar_one_or_none()

        if not old_quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        await db.delete(old_quiz)
        await db.commit()
        return {"message": "Quiz deleted successfully"}

    except Exception as e:
        await db.rollback()
        print(f"Error deleting quiz: {e}")
        raise HTTPException(status_code=400, detail=str(e))
