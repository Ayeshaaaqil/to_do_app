from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import uuid
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
import os
from sqlmodel import SQLModel, Session, select
from uuid import UUID
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import the chat API router
from src.api.chat import router as chat_router
from src.database.database import engine, get_session
from src.models.user import User
from src.models.todo import Todo

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Todo API", version="0.1.0")

# Include the chat API router with /api prefix
app.include_router(chat_router, prefix="/api")

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

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(credentials = Depends(security)):
    try:
        token = credentials.credentials
        user_id = verify_token(token)
        return user_id
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    try:
        # Import all models to register them with SQLModel
        from src.models.conversation import Conversation, ConversationMessage
        from src.models.user import User
        from src.models.todo import Todo

        # Create all tables
        SQLModel.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Signup endpoint
@app.post("/api/auth/signup", response_model=TokenResponse)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    try:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Create new user
        user_id = uuid.uuid4()
        user = User(
            id=user_id,
            email=user_create.email,
            name=user_create.name,
            hashed_password=user_create.password  # In real app, use bcrypt.hashpw()
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        logger.info(f"User created successfully: {user.email}")

        return {
            "user": UserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name
            ),
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        session.rollback()  # Rollback on HTTP exceptions
        raise
    except Exception as e:
        session.rollback()  # Rollback on any other exceptions
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during signup"
        )

# Signin endpoint
@app.post("/api/auth/signin", response_model=TokenResponse)
def signin(signin_data: SigninRequest, session: Session = Depends(get_session)):
    try:
        # Check if user exists in database
        user = session.exec(select(User).where(User.email == signin_data.email)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check password
        if signin_data.password != user.hashed_password:  # In real app, use bcrypt.checkpw()
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

        logger.info(f"User signed in successfully: {user.email}")

        return {
            "user": UserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name
            ),
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        session.rollback()  # Rollback on HTTP exceptions
        raise
    except Exception as e:
        session.rollback()  # Rollback on any other exceptions
        logger.error(f"Error during signin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during signin"
        )

# Signout endpoint
@app.post("/api/auth/signout")
def signout():
    return {"message": "Successfully signed out"}

# Todos endpoints
@app.get("/api/todos")
def get_todos(current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        user_uuid = UUID(current_user_id)
        todos = session.exec(select(Todo).where(Todo.user_id == user_uuid)).all()
        return todos
    except Exception as e:
        logger.error(f"Error getting todos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred retrieving todos"
        )

from pydantic import BaseModel

# Define request models
class CreateTodoRequest(BaseModel):
    title: str
    description: str = ""

class UpdateTodoRequest(BaseModel):
    title: str = None
    description: str = None

@app.post("/api/todos")
def create_todo(request: CreateTodoRequest, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        user_uuid = UUID(current_user_id)

        # Validate required fields
        if not request.title or not request.title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Title is required and cannot be empty"
            )

        todo = Todo(
            title=request.title.strip(),
            description=request.description,
            user_id=user_uuid
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    except HTTPException:
        session.rollback()  # Rollback on HTTP exceptions
        raise
    except Exception as e:
        session.rollback()  # Rollback on any other exceptions
        logger.error(f"Error creating todo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred creating the todo"
        )

@app.put("/api/todos/{id}")
def update_todo(id: str, request: UpdateTodoRequest, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        user_uuid = UUID(current_user_id)
        todo_uuid = UUID(id)

        todo = session.get(Todo, todo_uuid)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        if todo.user_id != user_uuid:
            raise HTTPException(status_code=403, detail="Not authorized to update this todo")

        # Update fields if provided
        if request.title is not None:
            if not request.title.strip():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Title cannot be empty"
                )
            todo.title = request.title.strip()
        if request.description is not None:
            todo.description = request.description

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    except HTTPException:
        session.rollback()  # Rollback on HTTP exceptions
        raise
    except Exception as e:
        session.rollback()  # Rollback on any other exceptions
        logger.error(f"Error updating todo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred updating the todo"
        )

@app.patch("/api/todos/{id}/complete")
def toggle_todo_complete(id: str, is_completed: bool, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        user_uuid = UUID(current_user_id)
        todo_uuid = UUID(id)

        todo = session.get(Todo, todo_uuid)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        if todo.user_id != user_uuid:
            raise HTTPException(status_code=403, detail="Not authorized to update this todo")

        todo.is_completed = is_completed

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    except HTTPException:
        session.rollback()  # Rollback on HTTP exceptions
        raise
    except Exception as e:
        session.rollback()  # Rollback on any other exceptions
        logger.error(f"Error toggling todo completion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred updating the todo"
        )

@app.delete("/api/todos/{id}")
def delete_todo(id: str, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        user_uuid = UUID(current_user_id)
        todo_uuid = UUID(id)

        todo = session.get(Todo, todo_uuid)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        if todo.user_id != user_uuid:
            raise HTTPException(status_code=403, detail="Not authorized to delete this todo")

        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}
    except HTTPException:
        session.rollback()  # Rollback on HTTP exceptions
        raise
    except Exception as e:
        session.rollback()  # Rollback on any other exceptions
        logger.error(f"Error deleting todo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred deleting the todo"
        )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")