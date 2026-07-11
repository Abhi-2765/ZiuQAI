# backend/app/routers/quizes.py
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel
from typing import List

from ..schemas.quizes import QuizCreate, QuizUpdate, QuizResponse, QuizDelete
from ..models.quizes import Quiz
from ..models.participants import Participant
from ..models.questions import Question, QuestionType
from ..models.user_responses import UserResponse as UserResponseModel
from ..db.base import get_db

router = APIRouter()

@router.post("/create", response_model=QuizResponse)
async def create_quiz(request: Request, quiz: QuizCreate, db: AsyncSession = Depends(get_db)):
    uid = getattr(request.state, "uid", None)
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    new_quiz = Quiz(
        quiz_name=quiz.quiz_name, question_count=quiz.question_count,
        quiz_difficulty=quiz.quiz_difficulty, quiz_start_time=quiz.quiz_start_time,
        quiz_duration=quiz.quiz_duration, show_leaderboard=quiz.show_leaderboard,
        status="draft", creator_uid=uid,
        question_types=quiz.question_types
    )
    db.add(new_quiz)
    await db.commit()
    await db.refresh(new_quiz)
    return new_quiz

@router.put("/update", response_model=QuizResponse)
async def update_quiz(request: Request, quiz: QuizUpdate, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    result = await db.execute(select(Quiz).where(Quiz.id == quiz.quiz_id, Quiz.creator_uid == uid))
    old_quiz = result.scalar_one_or_none()
    if not old_quiz: raise HTTPException(status_code=404, detail="Quiz not found")
    
    old_quiz.quiz_name = quiz.quiz_name
    old_quiz.question_count = quiz.question_count
    old_quiz.quiz_difficulty = quiz.quiz_difficulty
    old_quiz.quiz_start_time = quiz.quiz_start_time
    old_quiz.quiz_duration = quiz.quiz_duration
    old_quiz.show_leaderboard = quiz.show_leaderboard
    old_quiz.status = quiz.status
    if quiz.question_types is not None:
        old_quiz.question_types = quiz.question_types
    
    await db.commit()
    await db.refresh(old_quiz)
    return old_quiz

@router.delete("/delete")
async def delete_quiz(request: Request, quiz: QuizDelete, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    result = await db.execute(select(Quiz).where(Quiz.id == quiz.quiz_id, Quiz.creator_uid == uid))
    old_quiz = result.scalar_one_or_none()
    if not old_quiz: raise HTTPException(status_code=404, detail="Quiz not found")
    await db.delete(old_quiz)
    await db.commit()
    return {"message": "Quiz deleted successfully"}

@router.get("/my-quizzes", response_model=List[QuizResponse])
async def get_my_quizzes(request: Request, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    result = await db.execute(select(Quiz).where(Quiz.creator_uid == uid).order_by(Quiz.created_at.desc()))
    return result.scalars().all()

@router.get("/my-drafts")
async def get_my_drafts(request: Request, db: AsyncSession = Depends(get_db)):
    """Return draft quizzes for the current user with resource count."""
    uid = getattr(request.state, "uid", None)
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    result = await db.execute(
        select(Quiz).where(Quiz.creator_uid == uid, Quiz.status == "draft")
        .order_by(Quiz.created_at.desc())
    )
    drafts = result.scalars().all()
    
    from ..models.quiz_resource import QuizResource
    from sqlalchemy import func as sqlfunc
    
    out = []
    for d in drafts:
        res_count = await db.execute(
            select(sqlfunc.count()).where(QuizResource.quiz_id == d.id)
        )
        count = res_count.scalar() or 0
        out.append({
            "quiz_id": d.id,
            "quiz_name": d.quiz_name,
            "question_count": d.question_count,
            "quiz_difficulty": d.quiz_difficulty.value,
            "quiz_duration": d.quiz_duration,
            "question_types": d.question_types,
            "created_at": d.created_at.isoformat() if d.created_at else None,
            "resource_count": count,
        })
    return out

@router.post("/{quiz_id}/publish")
async def publish_quiz(quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id, Quiz.creator_uid == uid))
    quiz = result.scalar_one_or_none()
    if not quiz: raise HTTPException(status_code=404, detail="Quiz not found")
    quiz.status = "published"
    await db.commit()
    
    # Cleanup uploaded files after publish
    from ..routers.ingest import cleanup_quiz_uploads
    cleanup_quiz_uploads(quiz_id)
    
    return {"message": "Quiz published successfully"}

@router.get("/{quiz_id}")
async def get_quiz_details(quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz: raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Check if participant is already registered
    part_result = await db.execute(select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid))
    registered = part_result.scalar_one_or_none() is not None
    
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
        "status": quiz.status
    }

@router.post("/{quiz_id}/register")
async def register_for_quiz(quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Check if quiz exists
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz: raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Add participant
    existing = await db.execute(select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid))
    if existing.scalar_one_or_none():
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
async def get_quiz_questions(quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    # Verify participant
    part_result = await db.execute(select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid))
    participant = part_result.scalar_one_or_none()
    if not participant: raise HTTPException(status_code=403, detail="Not registered for this quiz")
    
    result = await db.execute(select(Question).where(Question.quiz_id == quiz_id))
    questions = result.scalars().all()
    
    # Strip correct answer
    out = []
    for q in questions:
        out.append({
            "id": q.id,
            "question": q.question,
            "question_type": q.question_type.value,
            "options": q.options
        })
    return out

class SubmitResponses(BaseModel):
    responses: dict # {question_id: response}

@router.post("/{quiz_id}/attempt/submit")
async def submit_quiz(quiz_id: int, req: SubmitResponses, request: Request, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    
    part_result = await db.execute(select(Participant).where(Participant.quiz_id == quiz_id, Participant.user_id == uid))
    participant = part_result.scalar_one_or_none()
    if not participant: raise HTTPException(status_code=403, detail="Not registered for this quiz")
    
    # Compute score
    questions_res = await db.execute(select(Question).where(Question.quiz_id == quiz_id))
    questions = questions_res.scalars().all()
    
    correct_count = 0
    q_map = {str(q.id): q for q in questions}
    
    for qid, ans in req.responses.items():
        if qid in q_map and q_map[qid].correct_answer.lower() == str(ans).lower():
            correct_count += 1
            
        # save response
        ur = UserResponseModel(participant_id=participant.id, qid=int(qid), response=str(ans))
        db.add(ur)
        
    participant.score = correct_count
    await db.commit()
    return {"score": correct_count, "total": len(questions)}

@router.get("/{quiz_id}/leaderboard")
async def get_leaderboard(quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Get quiz and check if ended
    quiz_res = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = quiz_res.scalar_one_or_none()
    if not quiz: raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Lock leaderboard check
    from datetime import datetime, timezone, timedelta
    end_time = quiz.quiz_start_time + timedelta(minutes=quiz.quiz_duration)
    if datetime.now(timezone.utc) < end_time:
        raise HTTPException(status_code=403, detail="Leaderboard is locked until the quiz has ended")
    
    # Fetch participants and users
    from ..models.users import User
    result = await db.execute(
        select(Participant, User.username).join(User, Participant.user_id == User.uid)
        .where(Participant.quiz_id == quiz_id).order_by(Participant.score.desc())
    )
    
    leaderboard = []
    for rank, (part, username) in enumerate(result.all(), start=1):
        leaderboard.append({
            "position": rank,
            "name": username,
            "marksObtained": part.score,
            "totalMarks": quiz.question_count
        })
    return leaderboard

@router.post("/{quiz_id}/generate")
async def generate_quiz_ai(quiz_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid: raise HTTPException(status_code=401, detail="Unauthorized")
    
    from ..graph.quiz_graph import run_quiz_pipeline
    from ..models.quiz_resource import QuizResource
    from ..services.ingestion.parser import FileParser
    import os
    
    quiz_res = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = quiz_res.scalar_one_or_none()
    if not quiz: raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Read & parse all local files for this quiz
    resources_res = await db.execute(
        select(QuizResource).where(QuizResource.quiz_id == quiz_id)
    )
    resources = resources_res.scalars().all()
    
    parser = FileParser()
    all_text_parts = []
    for resource in resources:
        if os.path.exists(resource.file_path):
            try:
                text = parser.parse_local_file(resource.file_path)
                if text and text.strip():
                    all_text_parts.append(text)
            except Exception as e:
                print(f"Warning: failed to parse {resource.filename}: {e}")
    
    context = "\n\n".join(all_text_parts)
    if not context.strip():
        raise HTTPException(status_code=400, detail="No readable content found in uploaded files.")
    
    # Read question_types from DB (fallback to defaults)
    q_types = quiz.question_types or ["mcq", "scq", "tof"]
    questions = await run_quiz_pipeline(
        quiz_id, quiz.question_count, quiz.quiz_difficulty.value, q_types,
        context=context
    )
    
    if not questions:
        raise HTTPException(status_code=500, detail="Failed to generate questions. AI model quota might be exhausted or unavailable.")
    
    # Delete existing questions
    await db.execute(delete(Question).where(Question.quiz_id == quiz_id))
    
    # Save new questions
    saved_qs = []
    for q in questions:
        db_q = Question(
            quiz_id=quiz_id,
            question=q["question"],
            question_type=QuestionType(q["question_type"].strip().lower()),
            correct_answer=q["correct_answer"],
            options=q.get("options")
        )
        db.add(db_q)
        saved_qs.append(db_q)
        
    await db.commit()
    
    out = []
    for q in saved_qs:
        out.append({
            "id": q.id,
            "question": q.question,
            "question_type": q.question_type.value,
            "options": q.options
        })
    return out
