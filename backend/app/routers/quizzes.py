# backend/app/routers/quizzes.py
import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel

from app.database import get_db
from app.models.quizes import Quiz
from app.models.questions import Question, QuestionType
from app.models.participants import Participant
from app.models.user_responses import UserResponse
from app.models.users import User
from app.models.quiz_resource import QuizResource
from app.schemas.quizes import QuizCreate, QuizUpdate, QuizResponse, QuizDelete
from app.routers.ingestion import extract_text, cleanup_quiz_directory
from app.ai.graph import run_quiz_pipeline
from app.models.chunk import Chunk
from app.ai.embedding_provider import generate_query_embedding

router = APIRouter()

def get_current_uid(request: Request) -> str:
    uid = getattr(request.state, "uid", None)
    if not uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return uid

@router.post("/create", response_model=QuizResponse)
async def create_quiz(
    request: Request, quiz_data: QuizCreate, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    new_quiz = Quiz(
        quiz_name=quiz_data.quiz_name,
        question_count=quiz_data.question_count,
        quiz_difficulty=quiz_data.quiz_difficulty,
        quiz_start_time=quiz_data.quiz_start_time,
        quiz_duration=quiz_data.quiz_duration,
        show_leaderboard=quiz_data.show_leaderboard,
        status=quiz_data.status,
        creator_uid=uid,
        question_types=quiz_data.question_types
    )
    db.add(new_quiz)
    await db.commit()
    await db.refresh(new_quiz)
    return new_quiz

@router.put("/update", response_model=QuizResponse)
async def update_quiz(
    request: Request, quiz_data: QuizUpdate, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    result = await db.execute(
        select(Quiz).where(Quiz.id == quiz_data.quiz_id, Quiz.creator_uid == uid)
    )
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz_data.quiz_name is not None:
        quiz.quiz_name = quiz_data.quiz_name
    if quiz_data.question_count is not None:
        quiz.question_count = quiz_data.question_count
    if quiz_data.quiz_difficulty is not None:
        quiz.quiz_difficulty = quiz_data.quiz_difficulty
    if quiz_data.quiz_start_time is not None:
        if quiz.quiz_start_time.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
            if quiz_data.quiz_start_time.replace(tzinfo=timezone.utc) != quiz.quiz_start_time.replace(tzinfo=timezone.utc):
                raise HTTPException(status_code=400, detail="Cannot change start time after the quiz has started.")
        quiz.quiz_start_time = quiz_data.quiz_start_time
    if quiz_data.quiz_duration is not None:
        quiz.quiz_duration = quiz_data.quiz_duration
    if quiz_data.show_leaderboard is not None:
        quiz.show_leaderboard = quiz_data.show_leaderboard
    if quiz_data.status is not None:
        quiz.status = quiz_data.status
    if quiz_data.question_types is not None:
        quiz.question_types = quiz_data.question_types

    await db.commit()
    await db.refresh(quiz)
    return quiz

@router.delete("/delete")
async def delete_quiz(
    request: Request, quiz_data: QuizDelete, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    result = await db.execute(
        select(Quiz).where(Quiz.id == quiz_data.quiz_id, Quiz.creator_uid == uid)
    )
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    await db.delete(quiz)
    await db.commit()
    return {"message": "Quiz deleted successfully"}

@router.get("/my-quizzes", response_model=List[QuizResponse])
async def get_my_quizzes(
    request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    result = await db.execute(
        select(Quiz).where(Quiz.creator_uid == uid).order_by(Quiz.created_at.desc())
    )
    return result.scalars().all()

@router.get("/my-drafts")
async def get_my_drafts(
    request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    # Join Quiz with QuizResource to count resources
    stmt = (
        select(Quiz, func.count(QuizResource.id).label("resource_count"))
        .outerjoin(QuizResource, Quiz.id == QuizResource.quiz_id)
        .where(Quiz.creator_uid == uid, Quiz.status == "draft")
        .group_by(Quiz.id)
        .order_by(Quiz.created_at.desc())
    )
    result = await db.execute(stmt)
    
    out = []
    for draft, count in result.all():
        out.append({
            "quiz_id": draft.id,
            "quiz_name": draft.quiz_name,
            "question_count": draft.question_count,
            "quiz_difficulty": draft.quiz_difficulty.value,
            "quiz_duration": draft.quiz_duration,
            "question_types": draft.question_types,
            "created_at": draft.created_at.isoformat() if draft.created_at else None,
            "resource_count": count,
        })
    return out

@router.post("/{quiz_id}/publish")
async def publish_quiz(
    quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    result = await db.execute(
        select(Quiz).where(Quiz.id == quiz_id, Quiz.creator_uid == uid)
    )
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz.status = "published"
    await db.commit()

    cleanup_quiz_directory(quiz_id)
    return {"message": "Quiz published successfully"}

@router.get("/{quiz_id}")
async def get_quiz_details(
    quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    p_result = await db.execute(
        select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid)
    )
    participant = p_result.scalar_one_or_none()
    registered = participant is not None
    submitted = participant.submitted if participant else False

    return {
        "id": quiz.id,
        "quiz_name": quiz.quiz_name,
        "quiz_start_time": quiz.quiz_start_time,
        "quiz_duration": quiz.quiz_duration,
        "question_count": quiz.question_count,
        "quiz_difficulty": quiz.quiz_difficulty.value,
        "question_types": quiz.question_types,
        "show_leaderboard": quiz.show_leaderboard,
        "registered": registered,
        "submitted": submitted,
        "status": quiz.status,
        "is_owner": quiz.creator_uid == uid
    }

@router.post("/{quiz_id}/register")
async def register_for_quiz(
    quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    p_result = await db.execute(
        select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid)
    )
    existing = p_result.scalar_one_or_none()
    if existing:
        return {
            "message": "Already registered",
            "quiz_name": quiz.quiz_name,
            "quiz_start_time": quiz.quiz_start_time,
            "quiz_duration": quiz.quiz_duration,
            "question_count": quiz.question_count
        }

    participant = Participant(quiz_id=quiz_id, user_id=uid, score=0.0)
    db.add(participant)
    await db.commit()

    return {
        "message": "Registered successfully",
        "quiz_name": quiz.quiz_name,
        "quiz_start_time": quiz.quiz_start_time,
        "quiz_duration": quiz.quiz_duration,
        "question_count": quiz.question_count
    }

@router.get("/{quiz_id}/attempt/questions")
async def get_quiz_questions(
    quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    p_result = await db.execute(
        select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid)
    )
    participant = p_result.scalar_one_or_none()
    if not participant:
        raise HTTPException(status_code=403, detail="Not registered for this quiz")
    if participant.submitted:
        raise HTTPException(status_code=403, detail="Quiz attempt already submitted")

    result = await db.execute(select(Question).where(Question.quiz_id == quiz_id))
    questions = result.scalars().all()
    
    return [
        {
            "id": q.id,
            "question": q.question,
            "question_type": q.question_type.value,
            "options": q.options
        }
        for q in questions
    ]

@router.get("/{quiz_id}/attempt/responses")
async def get_attempt_responses(
    quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    p_result = await db.execute(
        select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid)
    )
    participant = p_result.scalar_one_or_none()
    if not participant:
        raise HTTPException(status_code=403, detail="Not registered for this quiz")

    ur_result = await db.execute(
        select(UserResponse).where(UserResponse.participant_id == participant.id)
    )
    responses = {
        str(ur.qid): ur.response
        for ur in ur_result.scalars().all()
        if ur.response is not None and ur.response != "None"
    }
    return {"responses": responses}

class SubmitResponses(BaseModel):
    responses: Dict[str, Any]

@router.post("/{quiz_id}/attempt/save")
async def save_attempt_responses(
    quiz_id: int, req: SubmitResponses, request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    p_result = await db.execute(
        select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid)
    )
    participant = p_result.scalar_one_or_none()
    if not participant:
        raise HTTPException(status_code=403, detail="Not registered for this quiz")
    if participant.submitted:
        raise HTTPException(status_code=403, detail="Quiz attempt already submitted")

    existing_ur_result = await db.execute(
        select(UserResponse).where(UserResponse.participant_id == participant.id)
    )
    existing_urs = {ur.qid: ur for ur in existing_ur_result.scalars().all()}

    for qid, ans in req.responses.items():
        if ans is None:
            continue
        try:
            qid_int = int(qid)
        except (ValueError, TypeError):
            continue

        if qid_int in existing_urs:
            existing_urs[qid_int].response = str(ans)
        else:
            db.add(UserResponse(participant_id=participant.id, qid=qid_int, response=str(ans)))

    await db.commit()
    return {"message": "Responses saved successfully"}

@router.post("/{quiz_id}/attempt/submit")
async def submit_quiz(
    quiz_id: int, req: SubmitResponses, request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    p_result = await db.execute(
        select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid)
    )
    participant = p_result.scalar_one_or_none()
    if not participant:
        raise HTTPException(status_code=403, detail="Not registered for this quiz")
    if participant.submitted:
        raise HTTPException(status_code=400, detail="Quiz attempt already submitted")

    q_result = await db.execute(select(Question).where(Question.quiz_id == quiz_id))
    questions = q_result.scalars().all()
    q_map = {str(q.id): q for q in questions}

    existing_ur_result = await db.execute(
        select(UserResponse).where(UserResponse.participant_id == participant.id)
    )
    existing_urs = {ur.qid: ur for ur in existing_ur_result.scalars().all()}

    correct_count = 0
    for qid, ans in req.responses.items():
        if qid in q_map:
            q_obj = q_map[qid]
            target_correct = q_obj.correct_answer or ""
            user_ans = str(ans) if ans is not None else ""

            if q_obj.question_type == QuestionType.MCQ:
                target_set = {s.strip().lower() for s in target_correct.split(",") if s.strip()}
                user_set = {s.strip().lower() for s in user_ans.split(",") if s.strip()}
                if target_set and target_set == user_set:
                    correct_count += 1
            else:
                if target_correct.strip().lower() == user_ans.strip().lower():
                    correct_count += 1

        try:
            qid_int = int(qid)
            resp_str = str(ans) if ans is not None else None
            if qid_int in existing_urs:
                existing_urs[qid_int].response = resp_str
            else:
                db.add(UserResponse(participant_id=participant.id, qid=qid_int, response=resp_str))
        except (ValueError, TypeError):
            continue

    participant.score = float(correct_count)
    participant.submitted = True
    participant.submitted_at = datetime.now(timezone.utc)
    await db.commit()
    
    return {"score": correct_count, "total": len(questions)}

@router.get("/{quiz_id}/leaderboard")
async def get_leaderboard(
    quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    is_owner = (quiz.creator_uid == uid)

    if not is_owner:
        if not quiz.show_leaderboard:
            raise HTTPException(status_code=403, detail="Leaderboard visibility is disabled by the quiz owner")

        start_time = quiz.quiz_start_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        else:
            start_time = start_time.astimezone(timezone.utc)

        end_time = start_time + timedelta(minutes=quiz.quiz_duration)
        if datetime.now(timezone.utc) < end_time:
            raise HTTPException(status_code=403, detail="Leaderboard is locked until the quiz has ended")

    l_result = await db.execute(
        select(Participant, User.username)
        .join(User, Participant.user_id == User.uid)
        .where(Participant.quiz_id == quiz_id)
        .order_by(Participant.score.desc())
    )
    
    out = []
    for rank, (part, username) in enumerate(l_result.all(), start=1):
        out.append({
            "position": rank,
            "name": username,
            "marksObtained": part.score,
            "totalMarks": quiz.question_count
        })
    return out

@router.post("/{quiz_id}/generate")
async def generate_quiz_ai(
    quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    result = await db.execute(
        select(Quiz).where(Quiz.id == quiz_id, Quiz.creator_uid == uid)
    )
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    query_text = quiz.quiz_name + f" ({quiz.quiz_difficulty.value} level quiz topics)"
    try:
        query_embedding = await generate_query_embedding(query_text)
        
        stmt = (
            select(Chunk)
            .where(Chunk.quiz_id == quiz_id)
            .order_by(Chunk.embedding.l2_distance(query_embedding))
            .limit(15)
        )
        result = await db.execute(stmt)
        top_chunks = result.scalars().all()
        
        if not top_chunks:
            raise HTTPException(status_code=400, detail="No readable content found in uploaded files.")
            
        context = "\n\n".join([chunk.content for chunk in top_chunks])
    except HTTPException:
        raise
    except Exception as e:
        print(f"RAG retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve context for quiz generation.")

    q_types = quiz.question_types or ["mcq", "scq", "tof"]
    generated = await run_quiz_pipeline(
        quiz_id, quiz.question_count, quiz.quiz_difficulty.value, q_types, context=context
    )

    if not generated:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate questions. AI model quota might be exhausted or unavailable."
        )

    # Delete existing questions
    q_result = await db.execute(select(Question).where(Question.quiz_id == quiz_id))
    existing_questions = q_result.scalars().all()
    for eq in existing_questions:
        await db.delete(eq)
    await db.commit()

    db_questions = []
    for q in generated:
        db_q = Question(
            quiz_id=quiz_id,
            question=q["question"],
            question_type=QuestionType(q["question_type"].strip().lower()),
            correct_answer=q["correct_answer"],
            options=q.get("options")
        )
        db.add(db_q)
        db_questions.append(db_q)

    await db.commit()
    for db_q in db_questions:
        await db.refresh(db_q)

    return [
        {
            "id": q.id,
            "question": q.question,
            "question_type": q.question_type.value,
            "options": q.options
        }
        for q in db_questions
    ]

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    request: Request, db: AsyncSession = Depends(get_db)
):
    uid = get_current_uid(request)
    
    # Hosted count
    hosted_result = await db.execute(select(func.count(Quiz.id)).where(Quiz.creator_uid == uid))
    hosted_count = hosted_result.scalar_one_or_none() or 0
    
    # Attempted count
    attempted_result = await db.execute(
        select(func.count(Participant.id)).where(Participant.user_id == uid, Participant.submitted == True)
    )
    attempted_count = attempted_result.scalar_one_or_none() or 0
    
    # Recent activity
    recent_result = await db.execute(
        select(Participant, Quiz)
        .join(Quiz, Participant.quiz_id == Quiz.id)
        .where(Participant.user_id == uid, Participant.submitted == True)
        .order_by(Participant.submitted_at.desc())
        .limit(4)
    )
    
    recent_activity = []
    for part, quiz in recent_result.all():
        percentage = 0
        if quiz.question_count > 0:
            percentage = int((part.score / quiz.question_count) * 100)
            
        recent_activity.append({
            "quizName": quiz.quiz_name,
            "date": part.submitted_at.isoformat() if part.submitted_at else None,
            "score": int(part.score) if part.score.is_integer() else part.score,
            "total": quiz.question_count,
            "percentage": percentage,
            "difficulty": quiz.quiz_difficulty.value
        })
        
    return {
        "hostedCount": hosted_count,
        "attemptedCount": attempted_count,
        "recentActivity": recent_activity
    }

