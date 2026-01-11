"""
MCP Server Implementation for Todo Management

This module implements the Model Context Protocol server that exposes
todo operations as standardized tools for the AI agent to use.
"""
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel, Field
import json


class ToolCall(BaseModel):
    """Represents a call to an MCP tool"""
    tool_name: str
    parameters: Dict[str, Any]


class ToolResult(BaseModel):
    """Represents the result of an MCP tool call"""
    success: bool
    data: Any = None
    error: str = None


class MCPServer:
    """Model Context Protocol Server for Todo Management"""
    
    def __init__(self):
        self.tools = {}
        self.register_default_tools()
    
    def register_tool(self, name: str, func):
        """Register a tool with the MCP server"""
        self.tools[name] = func
    
    def register_default_tools(self):
        """Register the default todo management tools"""
        from .tools.todo_tool import (
            CreateTodoTool,
            GetTodosTool,
            UpdateTodoTool,
            DeleteTodoTool,
            ToggleTodoCompletionTool
        )

        # Create instances of the tools
        create_todo_tool = CreateTodoTool()
        get_todos_tool = GetTodosTool()
        update_todo_tool = UpdateTodoTool()
        delete_todo_tool = DeleteTodoTool()
        toggle_completion_tool = ToggleTodoCompletionTool()

        # Register the tools with the server
        self.register_tool(create_todo_tool.name, create_todo_tool.execute)
        self.register_tool(get_todos_tool.name, get_todos_tool.execute)
        self.register_tool(update_todo_tool.name, update_todo_tool.execute)
        self.register_tool(delete_todo_tool.name, delete_todo_tool.execute)
        self.register_tool(toggle_completion_tool.name, toggle_completion_tool.execute)
    
    async def execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call and return the result"""
        if tool_call.tool_name not in self.tools:
            return ToolResult(
                success=False,
                error=f"Tool '{tool_call.tool_name}' not found"
            )
        
        try:
            # Execute the tool function with the provided parameters
            result = await self.tools[tool_call.tool_name](**tool_call.parameters)
            return ToolResult(success=True, data=result)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
    
    def get_tool_list(self) -> List[str]:
        """Get a list of available tools"""
        return list(self.tools.keys())


# Global MCP server instance
mcp_server = MCPServer()


def get_mcp_server():
    """Get the global MCP server instance"""
    return mcp_server