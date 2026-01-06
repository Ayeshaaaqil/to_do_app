from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import uuid
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Todo API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Pydantic models
class UserCreate(BaseModel):
    email: str
    name: Optional[str] = None
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]

class TokenResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str

class SigninRequest(BaseModel):
    email: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Mock database (in real app, you'd use a real database)
mock_users_db = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Signup endpoint
@app.post("/api/auth/signup", response_model=TokenResponse)
def signup(user_create: UserCreate):
    # Check if user already exists
    if user_create.email in mock_users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # Create new user (in real app, you'd hash the password)
    user_id = str(uuid.uuid4())
    user_data = {
        "id": user_id,
        "email": user_create.email,
        "name": user_create.name,
        "hashed_password": user_create.password  # In real app, use bcrypt.hashpw()
    }
    mock_users_db[user_create.email] = user_data
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    
    return {
        "user": UserResponse(
            id=user_data["id"],
            email=user_data["email"],
            name=user_data["name"]
        ),
        "access_token": access_token,
        "token_type": "bearer"
    }

# Signin endpoint
@app.post("/api/auth/signin", response_model=TokenResponse)
def signin(user_data: SigninRequest):
    # Check if user exists in mock database
    user = mock_users_db.get(user_data.email)
    if not user or user_data.password != user["hashed_password"]:  # In real app, use bcrypt.checkpw()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )
    
    return {
        "user": UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"]
        ),
        "access_token": access_token,
        "token_type": "bearer"
    }

# Signout endpoint
@app.post("/api/auth/signout")
def signout():
    return {"message": "Successfully signed out"}

# Mock todos endpoints
@app.get("/api/todos")
def get_todos():
    return {"todos": [], "message": "Connected to API successfully"}

@app.post("/api/todos")
def create_todo():
    return {"message": "Todo created successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)