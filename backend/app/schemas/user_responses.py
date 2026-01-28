from pydantic import BaseModel

class UserResponseCreate(BaseModel):
    user_id: str
    quiz_id: int
    question_id: int
    session_id: int
    response: str

class UserResponseUpdate(BaseModel):
    user_id: str
    quiz_id: int
    question_id: int
    session_id: int
    response: str

class UserResponseDelete(BaseModel):
    user_id: str
    quiz_id: int
    question_id: int
    session_id: int

class UserResponseResponse(BaseModel):
    user_id: str
    quiz_id: int
    question_id: int
    session_id: int
    response: str
