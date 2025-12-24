from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.models.user import User
from app.schemas import UserCreate, UserLogin, Token, User as UserSchema, TokenData
from app.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
)
from app.services.logger import logger

router = APIRouter()

@router.post("/signup", response_model=UserSchema)
async def signup_user(user_data: UserCreate, db: AsyncSession = Depends(get_db_session)):
    logger.info(f"Attempting to sign up user: {user_data.email}")
    result = await db.execute(select(User).filter(User.email == user_data.email))
    db_user = result.scalars().first()
    if db_user:
        logger.warning(f"Signup failed: Email {user_data.email} already registered.")
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.email, # Use email as username for now
        hashed_password=hashed_password,
        software_background=user_data.software_background,
        hardware_background=user_data.hardware_background,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    logger.info(f"User {user_data.email} signed up successfully.")
    return db_user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db_session)
):
    logger.info(f"Attempting to log in user: {form_data.username}") # OAuth2PasswordRequestForm uses 'username' for identifier
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed: Invalid credentials for {form_data.username}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logger.info(f"User {form_data.username} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserSchema)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    logger.info(f"Fetching current user: {current_user.email}")
    return current_user

