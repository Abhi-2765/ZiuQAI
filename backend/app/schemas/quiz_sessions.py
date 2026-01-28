from pydantic import BaseModel

class QuizSessionCU(BaseModel):
    quiz_id: int
    user_id: str
    quiz_start_time: datetime 

class QuizSessionDelete(BaseModel):
    session_id: int

class QuizSessionResponse(BaseModel):
    session_id: int
    quiz_id: int
    user_id: str
    quiz_start_time: datetime 
