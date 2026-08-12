# backend/tests/test_quizes.py
import pytest
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.quizes import Quiz
from app.models.questions import Question
from app.models.participants import Participant

async def test_quiz_flow(client: AsyncClient, db_session: AsyncSession):
    # 1. Setup user & login
    register_payload = {
        "username": "hostuser",
        "email": "hostuser@example.com",
        "password": "password123"
    }
    await client.post("/auth/register", json=register_payload)
    login_res = await client.post("/auth/login", json={
        "email": "hostuser@example.com",
        "password": "password123"
    })
    token = login_res.cookies["access_token"]
    client.cookies.set("access_token", token)

    # 2. Create a Quiz (default draft)
    quiz_payload = {
        "quiz_name": "Test Science Quiz",
        "question_count": 2,
        "quiz_difficulty": "MEDIUM",
        "quiz_start_time": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        "quiz_duration": 10,
        "show_leaderboard": True
    }
    
    create_res = await client.post("/quizes/create", json=quiz_payload)
    assert create_res.status_code == 200
    quiz_data = create_res.json()
    assert quiz_data["status"] == "draft"
    quiz_id = quiz_data["id"]

    # 3. Add mock questions to the database for this quiz
    # (Since AI generation is tested separately, we populate mock ones here)
    q1 = Question(
        quiz_id=quiz_id,
        question="What is 2+2?",
        question_type="SCQ",
        correct_answer="4",
        options=["3", "4", "5"]
    )
    q2 = Question(
        quiz_id=quiz_id,
        question="Is earth flat?",
        question_type="TOF",
        correct_answer="False",
        options=["True", "False"]
    )
    db_session.add_all([q1, q2])
    await db_session.commit()
    
    # Reload questions to get their IDs
    result = await db_session.execute(select(Question).where(Question.quiz_id == quiz_id))
    db_questions = result.scalars().all()
    assert len(db_questions) == 2
    q1_id = db_questions[0].id
    q2_id = db_questions[1].id

    # 4. Register for the quiz
    reg_res = await client.post(f"/quizes/{quiz_id}/register")
    assert reg_res.status_code == 200
    assert "Registered" in reg_res.json()["message"]

    # Check quiz details - registered: True, submitted: False
    details_res = await client.get(f"/quizes/{quiz_id}")
    assert details_res.status_code == 200
    assert details_res.json()["registered"] is True
    assert details_res.json()["submitted"] is False

    # 5. Publish the quiz
    publish_res = await client.post(f"/quizes/{quiz_id}/publish")
    assert publish_res.status_code == 200

    # 6. Get attempt questions (strips answers)
    questions_res = await client.get(f"/quizes/{quiz_id}/attempt/questions")
    assert questions_res.status_code == 200
    attempt_questions = questions_res.json()
    assert len(attempt_questions) == 2
    assert "correct_answer" not in attempt_questions[0]
    assert attempt_questions[0]["options"] is not None

    # 7. Submit responses (1 correct, 1 incorrect)
    submit_payload = {
        "responses": {
            str(q1_id): "4",       # Correct
            str(q2_id): "True"      # Incorrect
        }
    }
    submit_res = await client.post(f"/quizes/{quiz_id}/attempt/submit", json=submit_payload)
    assert submit_res.status_code == 200
    submit_data = submit_res.json()
    assert submit_data["score"] == 1
    assert submit_data["total"] == 2

    # 8. Check quiz details after submit - submitted should now be True
    details_res_after = await client.get(f"/quizes/{quiz_id}")
    assert details_res_after.status_code == 200
    assert details_res_after.json()["submitted"] is True

    # 9. Verify subsequent attempt / submit requests are rejected
    questions_again = await client.get(f"/quizes/{quiz_id}/attempt/questions")
    assert questions_again.status_code == 403
    assert "already submitted" in questions_again.json()["detail"]

    submit_again = await client.post(f"/quizes/{quiz_id}/attempt/submit", json=submit_payload)
    assert submit_again.status_code == 400
    assert "already submitted" in submit_again.json()["detail"]
