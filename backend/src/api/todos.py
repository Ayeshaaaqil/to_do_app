from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database.database import get_session
from models.todo import Todo, TodoCreate, TodoRead, TodoUpdate, TodoPatch
from services import todo_service
from typing import List
import uuid
from .auth_middleware import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TodoRead])
def read_todos(session: Session = Depends(get_session), user_id: uuid.UUID = Depends(get_current_user)):
    todos = todo_service.get_todos(session, user_id)
    return todos

@router.post("/", response_model=TodoRead)
def create_todo(todo: TodoCreate, session: Session = Depends(get_session), user_id: uuid.UUID = Depends(get_current_user)):
    return todo_service.create_todo(session, todo, user_id)

@router.get("/{todo_id}", response_model=TodoRead)
def read_todo(todo_id: uuid.UUID, session: Session = Depends(get_session), user_id: uuid.UUID = Depends(get_current_user)):
    db_todo = todo_service.get_todo(session, todo_id, user_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: uuid.UUID, todo_update: TodoUpdate, session: Session = Depends(get_session), user_id: uuid.UUID = Depends(get_current_user)):
    db_todo = todo_service.update_todo(session, todo_id, todo_update, user_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.patch("/{todo_id}/complete", response_model=TodoRead)
def patch_todo_complete(todo_id: uuid.UUID, todo_patch: TodoPatch, session: Session = Depends(get_session), user_id: uuid.UUID = Depends(get_current_user)):
    db_todo = todo_service.patch_todo(session, todo_id, todo_patch, user_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: uuid.UUID, session: Session = Depends(get_session), user_id: uuid.UUID = Depends(get_current_user)):
    success = todo_service.delete_todo(session, todo_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}