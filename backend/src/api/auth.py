from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database.database import get_session
from models.user import UserCreate, UserRead
from services import auth_service
from typing import Dict
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup")
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    # Validate password length (bcrypt has a 72-byte limit)
    if len(user_create.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not exceed 72 bytes"
        )

    try:
        db_user = auth_service.create_user(session, user_create)

        # Create access token for the newly created user
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )

        return {
            "user": {
                "id": str(db_user.id),
                "email": db_user.email,
                "name": db_user.name
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.post("/signin")
def signin(user_data: Dict[str, str], session: Session = Depends(get_session)):
    email = user_data.get("email")
    password = user_data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    # Validate password length (bcrypt has a 72-byte limit)
    if len(password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not exceed 72 bytes"
        )

    user = auth_service.authenticate_user(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        },
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/signout")
def signout():
    # In a real implementation, you would invalidate the token
    return {"message": "Successfully signed out"}