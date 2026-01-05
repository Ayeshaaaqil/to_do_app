from sqlmodel import Session, select
from models.todo import Todo, TodoCreate, TodoUpdate, TodoPatch
from models.user import User
from typing import List, Optional
import uuid

def create_todo(session: Session, todo: TodoCreate, user_id: uuid.UUID) -> Todo:
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        is_completed=todo.is_completed,
        user_id=user_id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def get_todos(session: Session, user_id: uuid.UUID) -> List[Todo]:
    statement = select(Todo).where(Todo.user_id == user_id)
    return session.exec(statement).all()

def get_todo(session: Session, todo_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Todo]:
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    return session.exec(statement).first()

def update_todo(session: Session, todo_id: uuid.UUID, todo_update: TodoUpdate, user_id: uuid.UUID) -> Optional[Todo]:
    db_todo = get_todo(session, todo_id, user_id)
    if not db_todo:
        return None

    # Update the todo with provided values
    for field, value in todo_update.dict(exclude_unset=True).items():
        setattr(db_todo, field, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def patch_todo(session: Session, todo_id: uuid.UUID, todo_patch: TodoPatch, user_id: uuid.UUID) -> Optional[Todo]:
    db_todo = get_todo(session, todo_id, user_id)
    if not db_todo:
        return None

    # Update the todo with provided values
    for field, value in todo_patch.dict(exclude_unset=True).items():
        setattr(db_todo, field, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def delete_todo(session: Session, todo_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    db_todo = get_todo(session, todo_id, user_id)
    if not db_todo:
        return False

    session.delete(db_todo)
    session.commit()
    return True