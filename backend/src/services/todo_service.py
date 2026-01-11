"""
Todo Service Layer

This module provides business logic for todo operations,
separating concerns from the API layer and MCP tools.
"""
from typing import List, Optional
from sqlmodel import Session, select
from uuid import UUID
from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoPatch
from ..models.user import User


class TodoService:
    """Service layer for todo operations"""
    
    @staticmethod
    def create_todo(session: Session, todo: TodoCreate, user_id: UUID) -> Todo:
        """Create a new todo for a user"""
        db_todo = Todo.from_orm(todo)
        db_todo.user_id = user_id
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo
    
    @staticmethod
    def get_todo_by_id(session: Session, todo_id: UUID) -> Optional[Todo]:
        """Get a todo by its ID"""
        return session.get(Todo, todo_id)
    
    @staticmethod
    def get_todos_by_user(session: Session, user_id: UUID) -> List[Todo]:
        """Get all todos for a specific user"""
        statement = select(Todo).where(Todo.user_id == user_id)
        return session.exec(statement).all()
    
    @staticmethod
    def update_todo(session: Session, todo_id: UUID, todo_update: TodoUpdate) -> Optional[Todo]:
        """Update a todo with the provided values"""
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return None
        
        todo_data = todo_update.dict(exclude_unset=True)
        for key, value in todo_data.items():
            setattr(db_todo, key, value)
        
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo
    
    @staticmethod
    def patch_todo(session: Session, todo_id: UUID, todo_patch: TodoPatch) -> Optional[Todo]:
        """Partially update a todo with the provided values"""
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return None
        
        todo_data = todo_patch.dict(exclude_unset=True)
        for key, value in todo_data.items():
            setattr(db_todo, key, value)
        
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo
    
    @staticmethod
    def delete_todo(session: Session, todo_id: UUID) -> bool:
        """Delete a todo by its ID"""
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return False
        
        session.delete(db_todo)
        session.commit()
        return True
    
    @staticmethod
    def toggle_todo_completion(session: Session, todo_id: UUID, completed: bool) -> Optional[Todo]:
        """Toggle the completion status of a todo"""
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return None
        
        db_todo.is_completed = completed
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo