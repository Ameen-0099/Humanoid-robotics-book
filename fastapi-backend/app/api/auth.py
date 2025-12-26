from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.models.user import User
from app.schemas import UserCreate, UserLogin, Token, UserDisplay, TokenData, UserUpdate
from app.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
)
from app.services.logger import logger

router = APIRouter()

@router.post("/signup", response_model=UserDisplay)
async def signup_user(user_data: UserCreate, db: AsyncSession = Depends(get_db_session)):
    logger.info(f"Attempting to sign up user: {user_data.email}")
    result = await db.execute(select(User).filter(User.email == user_data.email))
    db_user = result.scalars().first()
    if db_user:
        logger.warning(f"Signup failed: Email {user_data.email} already registered.")
        raise HTTPException(status_code=400, detail="This email is already registered. Please try logging in or use a different email.")

    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name,
        software_background=user_data.software_background,
        hardware_background=user_data.hardware_background,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    logger.info(f"User {user_data.email} signed up successfully.")
    return db_user


@router.post("/sign-in/email-and-password", response_model=Token)
async def login_for_access_token(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db_session)
):
    logger.info(f"Attempting to log in user: {user_data.email}")
    result = await db.execute(select(User).filter(User.email == user_data.email))
    user = result.scalars().first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        logger.warning(f"Login failed: Invalid credentials for {user_data.email}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logger.info(f"User {user_data.email} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserDisplay)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    logger.info(f"Fetching current user: {current_user.email}")
    return current_user

@router.put("/users/me/", response_model=UserDisplay)
async def update_user_me(
    user_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db_session),
):
    logger.info(f"Updating profile for user: {current_user.email}")
    if user_data.name is not None:
        current_user.name = user_data.name
    if user_data.software_background is not None:
        current_user.software_background = user_data.software_background
    if user_data.hardware_background is not None:
        current_user.hardware_background = user_data.hardware_background

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    logger.info(f"Profile updated successfully for user: {current_user.email}")
    return current_user

