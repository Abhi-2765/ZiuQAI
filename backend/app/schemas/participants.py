from pydantic import BaseModel

class ParticipantCreate(BaseModel):
    session_id: int

class ParticipantInfo(BaseModel):
    session_id: int
    score: float

class ParticipantDelete(BaseModel):
    session_id: int
    user_id: int

class ParticipantResponse(BaseModel):
    participant_id: int
    session_id: int