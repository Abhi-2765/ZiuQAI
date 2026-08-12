# backend/app/routers/responses.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user_responses import UserResponse
from app.schemas.user_responses import (
    UserResponseCreate, UserResponseUpdate, UserResponseDelete, UserResponseResponse
)

router = APIRouter()

def get_current_uid(request: Request) -> str:
    uid = getattr(request.state, "uid", None)
    if not uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return uid

@router.post("/create", response_model=UserResponseResponse)
async def create_user_response(
    request: Request, user_response: UserResponseCreate, db: AsyncSession = Depends(get_db)
):
    get_current_uid(request)
    new_user_response = UserResponse(
        participant_id=user_response.participant_id,
        qid=user_response.question_id,
        response=user_response.response,
    )
    db.add(new_user_response)
    await db.commit()
    await db.refresh(new_user_response)
    return new_user_response

@router.put("/update", response_model=UserResponseResponse)
async def update_user_response(
    request: Request, user_response: UserResponseUpdate, db: AsyncSession = Depends(get_db)
):
    get_current_uid(request)
    result = await db.execute(
        select(UserResponse).where(UserResponse.id == user_response.user_response_id)
    )
    resp_obj = result.scalar_one_or_none()
    if not resp_obj:
        raise HTTPException(status_code=404, detail="User response not found")
    
    resp_obj.response = user_response.response
    await db.commit()
    await db.refresh(resp_obj)
    return resp_obj

@router.delete("/delete")
async def delete_user_response(
    request: Request, user_response: UserResponseDelete, db: AsyncSession = Depends(get_db)
):
    get_current_uid(request)
    result = await db.execute(
        select(UserResponse).where(UserResponse.id == user_response.user_response_id)
    )
    resp_obj = result.scalar_one_or_none()
    if not resp_obj:
        raise HTTPException(status_code=404, detail="User response not found")
    
    await db.delete(resp_obj)
    await db.commit()
    return {"message": "Response deleted successfully"}
