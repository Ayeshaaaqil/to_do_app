"""
Base MCP Tool Structure for Todo Operations

This module defines the base structure for MCP tools that perform todo operations.
All tools follow the same interface and error handling pattern.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class ToolResponse(BaseModel):
    """Base response structure for all MCP tools"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


class BaseMCPTool(ABC):
    """Abstract base class for all MCP tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResponse:
        """Execute the tool with the given parameters"""
        pass
    
    def validate_parameters(self, **kwargs) -> bool:
        """Validate the parameters passed to the tool"""
        # Default implementation - can be overridden by subclasses
        return True


class TodoMCPTool(BaseMCPTool):
    """Base class for all todo-related MCP tools"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
    
    async def execute(self, **kwargs) -> ToolResponse:
        """Execute the todo tool - to be implemented by subclasses"""
        try:
            if not self.validate_parameters(**kwargs):
                return ToolResponse(
                    success=False,
                    error="Invalid parameters provided"
                )
            
            result = await self.execute_todo_operation(**kwargs)
            return ToolResponse(success=True, data=result)
        
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {str(e)}")
            return ToolResponse(
                success=False,
                error=f"Error executing tool: {str(e)}"
            )
    
    @abstractmethod
    async def execute_todo_operation(self, **kwargs) -> Any:
        """Execute the specific todo operation - to be implemented by subclasses"""
        pass