from pydantic import BaseModel, Field
from ..models.quizes import Difficulty


class QuizCreate(BaseModel):
    quiz_name: str
    question_count: int
    quiz_difficulty: Difficulty
    quiz_duration: int
    show_leaderboard: bool = True


class QuizUpdate(BaseModel):
    quiz_id: int
    quiz_name: str
    question_count: int
    quiz_difficulty: Difficulty
    quiz_duration: int
    show_leaderboard: bool


class QuizDelete(BaseModel):
    quiz_id: int


class QuizResponse(BaseModel):
    quiz_id: int = Field(alias="id")
    quiz_name: str
    question_count: int
    quiz_difficulty: Difficulty
    quiz_duration: int
    show_leaderboard: bool

    class Config:
        from_attributes = True
        populate_by_name = True