from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .utils.auth_middleware import AuthMiddleware
from .db.base import get_db, Base, engine

# Routers
from .routers.auth import router as auth_router
from .routers.quizes import router as quizes_router

# DB models
from .models.users import User
from .models.quizes import Quiz
from .models.quiz_sessions import QuizSession
from .models.participants import Participant
from .models.user_responses import UserResponse
from .models.questions import Question
#import future models here so that Base will pick them else we will get errors

app = FastAPI(
    title="FastAPI + React",
    description="FastAPI + React",
    version="0.0.1",
    docs_url="/docs"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(quizes_router, prefix="/quizes", tags=["Quizes"])

# Events
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get(path="/", tags=["Root"])
async def listen():
    # response can be a "pydantic object" or "python dict" to be compatible with JSON
    return {"message": "Hello World"}
