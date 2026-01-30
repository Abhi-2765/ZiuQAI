from pydantic import BaseModel
from datetime import datetime

class QuizSessionCreate(BaseModel):
    quiz_id: int
    quiz_start_time: datetime 
    quiz_duration: int

class QuizSessionUpdate(BaseModel):
    session_id: int
    quiz_start_time: datetime 
class QuizSessionDelete(BaseModel):
    session_id: int

class QuizSessionResponse(BaseModel):
    id: int
    quiz_start_time: datetime 
    quiz_duration: int
