"""
Chat API Endpoint

This module implements the stateless chat API endpoint that accepts
user messages and returns AI-generated responses for todo management.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import json
from ..api.auth_middleware import get_current_user
from ..agents.todo_agent import TodoAgent
from ..services.conversation_service import ConversationService
from ..models.conversation import ConversationMessage
from ..database.database import get_session


router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    message_id: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user_id: UUID = Depends(get_current_user)
):
    """
    Process a user's natural language message and return an AI-generated response for todo management.

    This endpoint:
    1. Authenticates the user
    2. Retrieves conversation history from database
    3. Sends user message to AI agent
    4. Agent invokes MCP tools as needed
    5. Receives response from agent
    6. Stores new messages in conversation history
    7. Returns response to user
    """
    try:
        # Get a database session
        with next(get_session()) as session:
            # Get or create conversation
            conversation = None
            if request.conversation_id:
                # Try to get existing conversation
                conversation = ConversationService.get_conversation_by_id(
                    session,
                    UUID(request.conversation_id)
                )

                if not conversation or conversation.user_id != current_user_id:
                    raise HTTPException(
                        status_code=404,
                        detail="Conversation not found or access denied"
                    )
            else:
                # Create a new conversation
                conversation = ConversationService.create_conversation(
                    session,
                    current_user_id,
                    f"Conversation with {current_user_id}"
                )

            # Add user's message to the conversation
            user_message = ConversationService.add_message_to_conversation(
                session,
                conversation.id,
                "user",
                request.message
            )

            # Process the message with the AI agent
            agent = TodoAgent()
            agent_response = await agent.process_message(
                request.message,
                str(current_user_id),
                str(conversation.id)
            )

            # Add AI's response to the conversation
            ai_message = ConversationService.add_message_to_conversation(
                session,
                conversation.id,
                "assistant",
                agent_response["response"]
            )

            # Return the response
            return ChatResponse(
                response=agent_response["response"],
                conversation_id=str(conversation.id),
                message_id=str(ai_message.id) if ai_message else None
            )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other errors
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred processing your request: {str(e)}"
        )