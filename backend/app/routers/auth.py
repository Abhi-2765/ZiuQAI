from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from ..utils.auth_handler import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_user,
    get_user_by_uid,
    get_password_hash,
    get_current_active_user,
)
from ..db.base import get_db
from ..schemas.auth import UserCreate, UserResponse, UserLogin
from ..models.users import User

router = APIRouter()


@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    try:
        hashed_password = get_password_hash(user.password)
        uid = uuid.uuid4()

        db_user = User(
            uid=str(uid),
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return {"message": "User registered successfully, login to continue"}

    except Exception as e:
        await db.rollback()
        print(f"Error registering user: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    response: Response,
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    user_obj = await authenticate_user(db, user.email, user.password)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        uid=user_obj.uid,
        expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=int(access_token_expires.total_seconds()),
        path="/",
        samesite="lax",
        secure=False,  # True in production
    )

    return {
        "message": "Login successful",
        "email": user_obj.email,
        "username": user_obj.username
    }

@router.post("/logout")
async def logout(response: Response, db: AsyncSession = Depends(get_db)):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(request: Request, db: AsyncSession = Depends(get_db)):
    uid = request.state.uid
    if not uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = await get_user_by_uid(db, uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user