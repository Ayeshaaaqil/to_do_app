"""
MCP Tools for Todo Operations

This module implements the specific MCP tools for todo operations:
- create_todo
- get_todos
- update_todo
- delete_todo
- toggle_todo_completion
"""
from typing import Dict, Any, List
from uuid import UUID
import json
from sqlmodel import Session
from .base import TodoMCPTool, ToolResponse
from ...database.database import get_session
from ...services.todo_service import TodoService
from ...models.todo import TodoCreate


class CreateTodoTool(TodoMCPTool):
    """MCP Tool for creating a new todo"""
    
    def __init__(self):
        super().__init__(
            name="create_todo",
            description="Create a new todo item for a user"
        )
    
    def validate_parameters(self, title: str, user_token: str, **kwargs) -> bool:
        """Validate the parameters for creating a todo"""
        return title and len(title.strip()) > 0 and user_token
    
    async def execute_todo_operation(self, title: str, description: str = None, user_token: str = None, user_id: str = None) -> Dict[str, Any]:
        """Execute the create todo operation"""
        # In a real implementation, we would authenticate the user using the token
        # For now, we'll use the user_id passed directly
        
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)
        
        # Create a new todo using the service layer
        todo_create = TodoCreate(
            title=title,
            description=description
        )
        
        # Get a database session
        with next(get_session()) as session:
            new_todo = TodoService.create_todo(session, todo_create, user_uuid)
            
            # Return the created todo data
            return {
                "id": str(new_todo.id),
                "title": new_todo.title,
                "description": new_todo.description,
                "is_completed": new_todo.is_completed,
                "user_id": str(new_todo.user_id),
                "created_at": new_todo.created_at.isoformat()
            }


class GetTodosTool(TodoMCPTool):
    """MCP Tool for retrieving todos for a user"""
    
    def __init__(self):
        super().__init__(
            name="get_todos",
            description="Get all todo items for a user"
        )
    
    def validate_parameters(self, user_token: str, **kwargs) -> bool:
        """Validate the parameters for getting todos"""
        return user_token is not None
    
    async def execute_todo_operation(self, user_token: str = None, user_id: str = None) -> List[Dict[str, Any]]:
        """Execute the get todos operation"""
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)
        
        # Get a database session
        with next(get_session()) as session:
            todos = TodoService.get_todos_by_user(session, user_uuid)
            
            # Return the todos data
            return [
                {
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "is_completed": todo.is_completed,
                    "user_id": str(todo.user_id),
                    "created_at": todo.created_at.isoformat()
                }
                for todo in todos
            ]


class UpdateTodoTool(TodoMCPTool):
    """MCP Tool for updating a todo"""
    
    def __init__(self):
        super().__init__(
            name="update_todo",
            description="Update an existing todo item"
        )
    
    def validate_parameters(self, todo_id: str, user_token: str, **kwargs) -> bool:
        """Validate the parameters for updating a todo"""
        try:
            UUID(todo_id)  # Validate that todo_id is a valid UUID
            return user_token is not None
        except ValueError:
            return False
    
    async def execute_todo_operation(self, todo_id: str, title: str = None, description: str = None, user_token: str = None, user_id: str = None) -> Dict[str, Any]:
        """Execute the update todo operation"""
        # Convert IDs to UUIDs
        todo_uuid = UUID(todo_id)
        user_uuid = UUID(user_id)
        
        # Prepare update data
        from ..models.todo import TodoUpdate
        todo_update = TodoUpdate(
            title=title,
            description=description
        )
        
        # Get a database session
        with next(get_session()) as session:
            updated_todo = TodoService.update_todo(session, todo_uuid, todo_update)
            
            if updated_todo is None:
                raise ValueError(f"Todo with id {todo_id} not found")
            
            # Return the updated todo data
            return {
                "id": str(updated_todo.id),
                "title": updated_todo.title,
                "description": updated_todo.description,
                "is_completed": updated_todo.is_completed,
                "user_id": str(updated_todo.user_id),
                "created_at": updated_todo.created_at.isoformat(),
                "updated_at": updated_todo.updated_at.isoformat()
            }


class DeleteTodoTool(TodoMCPTool):
    """MCP Tool for deleting a todo"""
    
    def __init__(self):
        super().__init__(
            name="delete_todo",
            description="Delete an existing todo item"
        )
    
    def validate_parameters(self, todo_id: str, user_token: str, **kwargs) -> bool:
        """Validate the parameters for deleting a todo"""
        try:
            UUID(todo_id)  # Validate that todo_id is a valid UUID
            return user_token is not None
        except ValueError:
            return False
    
    async def execute_todo_operation(self, todo_id: str, user_token: str = None, user_id: str = None) -> Dict[str, Any]:
        """Execute the delete todo operation"""
        # Convert IDs to UUIDs
        todo_uuid = UUID(todo_id)
        user_uuid = UUID(user_id)
        
        # Get a database session
        with next(get_session()) as session:
            success = TodoService.delete_todo(session, todo_uuid)
            
            if not success:
                raise ValueError(f"Todo with id {todo_id} not found")
            
            # Return success confirmation
            return {
                "success": True,
                "message": f"Todo with id {todo_id} deleted successfully"
            }


class ToggleTodoCompletionTool(TodoMCPTool):
    """MCP Tool for toggling a todo's completion status"""
    
    def __init__(self):
        super().__init__(
            name="toggle_todo_completion",
            description="Toggle the completion status of a todo item"
        )
    
    def validate_parameters(self, todo_id: str, completed: bool, user_token: str, **kwargs) -> bool:
        """Validate the parameters for toggling todo completion"""
        try:
            UUID(todo_id)  # Validate that todo_id is a valid UUID
            return user_token is not None and isinstance(completed, bool)
        except ValueError:
            return False
    
    async def execute_todo_operation(self, todo_id: str, completed: bool, user_token: str = None, user_id: str = None) -> Dict[str, Any]:
        """Execute the toggle todo completion operation"""
        # Convert IDs to UUIDs
        todo_uuid = UUID(todo_id)
        user_uuid = UUID(user_id)
        
        # Get a database session
        with next(get_session()) as session:
            updated_todo = TodoService.toggle_todo_completion(session, todo_uuid, completed)
            
            if updated_todo is None:
                raise ValueError(f"Todo with id {todo_id} not found")
            
            # Return the updated todo data
            return {
                "id": str(updated_todo.id),
                "title": updated_todo.title,
                "description": updated_todo.description,
                "is_completed": updated_todo.is_completed,
                "user_id": str(updated_todo.user_id),
                "created_at": updated_todo.created_at.isoformat(),
                "updated_at": updated_todo.updated_at.isoformat()
            }