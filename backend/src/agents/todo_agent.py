"""
Todo Agent Definition for Todo Management

This module defines the AI agent that processes natural language input
and invokes tools to perform todo operations.
"""
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TodoAgent:
    """AI Agent for processing natural language todo requests"""

    def __init__(self):
        # Initialize without requiring OpenAI API key
        pass

    async def process_message(
        self,
        user_message: str,
        user_id: str,
        conversation_id: str = None
    ) -> Dict[str, Any]:
        """
        Process a user's natural language message and return an appropriate response.

        This method parses the intent from the user message and calls the appropriate tool.
        """
        try:
            # Validate the input first
            is_valid, error_msg = self._validate_input(user_message)
            if not is_valid:
                return {
                    "response": f"Input validation error: {error_msg}",
                    "action_taken": False
                }

            # Determine the intent from the user message
            intent = self._determine_intent(user_message)

            if intent == "create_todo":
                return await self._handle_create_todo(user_message, user_id)
            elif intent == "get_todos":
                return await self._handle_get_todos(user_id)
            elif intent == "update_todo":
                return await self._handle_update_todo(user_message, user_id)
            elif intent == "delete_todo":
                return await self._handle_delete_todo(user_message, user_id)
            elif intent == "toggle_completion":
                return await self._handle_toggle_completion(user_message, user_id)
            else:
                return {
                    "response": "I'm not sure how to help with that. You can ask me to create, view, update, delete, or mark todos as complete.",
                    "action_taken": False
                }

        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "action_taken": False
            }

    def _validate_input(self, message: str) -> tuple[bool, str]:
        """Validate user input and return (is_valid, error_message)"""
        if not message or not message.strip():
            return False, "Message cannot be empty"

        if len(message.strip()) < 3:
            return False, "Message is too short to process"

        # Add more validation rules as needed
        return True, ""

    def _determine_intent(self, message: str) -> str:
        """Determine the user's intent from their message"""
        message_lower = message.lower()

        if any(word in message_lower for word in ["create", "add", "new", "make"]):
            if any(word in message_lower for word in ["todo", "task", "do"]):
                return "create_todo"

        if any(word in message_lower for word in ["show", "list", "view", "get", "what"]):
            if any(word in message_lower for word in ["todo", "task", "todos", "tasks", "list"]):
                return "get_todos"

        if any(word in message_lower for word in ["update", "change", "modify", "edit"]):
            if any(word in message_lower for word in ["todo", "task"]):
                return "update_todo"

        if any(word in message_lower for word in ["delete", "remove", "cancel"]):
            if any(word in message_lower for word in ["todo", "task"]):
                return "delete_todo"

        if any(word in message_lower for word in ["complete", "done", "finish", "mark"]):
            if any(word in message_lower for word in ["todo", "task"]):
                return "toggle_completion"

        # Default to create if it seems like they're adding something
        if any(word in message_lower for word in ["buy", "call", "walk", "pick", "go"]):
            return "create_todo"

        return "unknown"

    async def _handle_create_todo(self, message: str, user_id: str) -> Dict[str, Any]:
        """Handle creating a new todo based on the user's message"""
        # Extract the todo title from the message
        title = self._extract_todo_title(message)

        if not title:
            return {
                "response": "I couldn't understand what todo you'd like to create. Please be more specific.",
                "action_taken": False
            }

        # Call the tool to create the todo
        from ..mcp.tools.todo_tool import CreateTodoTool
        tool = CreateTodoTool()

        try:
            # Execute the tool to create the todo
            result = await tool.execute_todo_operation(
                title=title,
                description="Created from natural language input",
                user_id=user_id
            )

            return {
                "response": f"I've created a new todo for you: '{result['title']}'.",
                "action_taken": True,
                "todo": result
            }
        except Exception as e:
            return {
                "response": f"Sorry, I couldn't create that todo: {str(e)}",
                "action_taken": False
            }

    async def _handle_get_todos(self, user_id: str) -> Dict[str, Any]:
        """Handle retrieving todos for the user"""
        # Call the tool to get todos
        from ..mcp.tools.todo_tool import GetTodosTool
        tool = GetTodosTool()

        try:
            # Execute the tool to get todos
            todos = await tool.execute_todo_operation(user_id=user_id)

            if not todos:
                response = "You don't have any todos yet."
            else:
                todo_list = "\n".join([f"- {todo['title']}" + (" (completed)" if todo['is_completed'] else "") for todo in todos])
                response = f"Here are your todos:\n{todo_list}"

            return {
                "response": response,
                "action_taken": True,
                "todos": todos
            }
        except Exception as e:
            return {
                "response": f"Sorry, I couldn't retrieve your todos: {str(e)}",
                "action_taken": False
            }

    async def _handle_update_todo(self, message: str, user_id: str) -> Dict[str, Any]:
        """Handle updating an existing todo"""
        # Extract the todo details from the message
        # This is a simplified implementation - in reality, you'd need more sophisticated NLP
        import re

        # Look for patterns like "update 'todo title' to 'new title'"
        match = re.search(r"update ['\"](.+?)['\"] to ['\"](.+?)['\"]", message, re.IGNORECASE)
        if not match:
            return {
                "response": "I couldn't understand which todo you'd like to update and what to change it to. Please use the format: update 'current title' to 'new title'.",
                "action_taken": False
            }

        old_title, new_title = match.groups()

        # Call the tool to update the todo
        from ..mcp.tools.todo_tool import UpdateTodoTool
        tool = UpdateTodoTool()

        try:
            # Execute the tool to update the todo
            # This would require finding the todo by title first
            # For now, we'll return a message indicating the limitation
            return {
                "response": f"I would update the todo '{old_title}' to '{new_title}', but finding todos by title is not fully implemented yet.",
                "action_taken": False
            }
        except Exception as e:
            return {
                "response": f"Sorry, I couldn't update that todo: {str(e)}",
                "action_taken": False
            }

    async def _handle_delete_todo(self, message: str, user_id: str) -> Dict[str, Any]:
        """Handle deleting a todo"""
        # Extract the todo title from the message
        title = self._extract_todo_title(message)

        if not title:
            return {
                "response": "I couldn't understand which todo you'd like to delete. Please be more specific.",
                "action_taken": False
            }

        # Call the tool to delete the todo
        from ..mcp.tools.todo_tool import DeleteTodoTool
        tool = DeleteTodoTool()

        try:
            # Execute the tool to delete the todo
            # This would require finding the todo by title first
            # For now, we'll return a message indicating the limitation
            return {
                "response": f"I would delete the todo '{title}', but finding todos by title is not fully implemented yet.",
                "action_taken": False
            }
        except Exception as e:
            return {
                "response": f"Sorry, I couldn't delete that todo: {str(e)}",
                "action_taken": False
            }

    async def _handle_toggle_completion(self, message: str, user_id: str) -> Dict[str, Any]:
        """Handle toggling a todo's completion status"""
        # Extract the todo title from the message
        title = self._extract_todo_title(message)

        if not title:
            return {
                "response": "I couldn't understand which todo you'd like to mark as complete/incomplete. Please be more specific.",
                "action_taken": False
            }

        # Determine if the user wants to mark as complete or incomplete
        message_lower = message.lower()
        completed = any(word in message_lower for word in ["complete", "done", "finished"])
        if not completed:
            completed = not any(word in message_lower for word in ["incomplete", "not done", "not finished"])

        # Call the tool to toggle completion
        from ..mcp.tools.todo_tool import ToggleTodoCompletionTool
        tool = ToggleTodoCompletionTool()

        try:
            # Execute the tool to toggle completion
            # This would require finding the todo by title first
            # For now, we'll return a message indicating the limitation
            return {
                "response": f"I would toggle the completion status of '{title}', but finding todos by title is not fully implemented yet.",
                "action_taken": False
            }
        except Exception as e:
            return {
                "response": f"Sorry, I couldn't toggle the completion status of that todo: {str(e)}",
                "action_taken": False
            }

    def _extract_todo_title(self, message: str) -> str:
        """Extract the todo title from a user's message"""
        import re

        # Look for patterns like "add 'buy groceries'", "create 'walk the dog'", etc.
        patterns = [
            r"(?:add|create|make|new) ['\"](.+?)['\"]",
            r"['\"](.+?)['\"]",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1)

        # If no quoted text found, try to extract the main action
        words = message.lower().split()
        if len(words) > 1:
            # Skip common starting words like "add", "create", etc.
            if words[0] in ["add", "create", "make", "new", "please", "can", "you"]:
                return " ".join(words[1:]).strip()

        return message.strip()