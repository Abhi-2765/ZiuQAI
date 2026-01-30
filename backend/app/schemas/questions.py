from pydantic import BaseModel, Field
from ..models.questions import QuestionType

class QuestionCreate(BaseModel):
    quiz_id: int
    question: str
    question_type: QuestionType
    correct_answer: str

class QuestionUpdate(BaseModel):
    question_id: int
    question: str
    question_type: QuestionType
    correct_answer: str

class QuestionDelete(BaseModel):
    question_id: int

class QuestionResponse(BaseModel):
    question_id: int = Field(alias="id")
    quiz_id: int
    question: str
    question_type: QuestionType
    correct_answer: str

    class Config:
        from_attributes = True
        populate_by_name = True
