"""
Conversation Service Layer

This module provides business logic for conversation operations,
separating concerns from the API layer and MCP tools.
"""
from typing import List, Optional
from sqlmodel import Session, select
from uuid import UUID
from ..models.conversation import Conversation, ConversationMessage


class ConversationService:
    """Service layer for conversation operations"""
    
    @staticmethod
    def create_conversation(session: Session, user_id: UUID, title: str) -> Conversation:
        """Create a new conversation for a user"""
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation
    
    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation by its ID"""
        return session.get(Conversation, conversation_id)
    
    @staticmethod
    def get_conversations_by_user(session: Session, user_id: UUID) -> List[Conversation]:
        """Get all conversations for a specific user"""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()
    
    @staticmethod
    def update_conversation(session: Session, conversation_id: UUID, title: str) -> Optional[Conversation]:
        """Update a conversation with the provided values"""
        db_conversation = session.get(Conversation, conversation_id)
        if not db_conversation:
            return None
        
        db_conversation.title = title
        session.add(db_conversation)
        session.commit()
        session.refresh(db_conversation)
        return db_conversation
    
    @staticmethod
    def delete_conversation(session: Session, conversation_id: UUID) -> bool:
        """Delete a conversation by its ID"""
        db_conversation = session.get(Conversation, conversation_id)
        if not db_conversation:
            return False
        
        session.delete(db_conversation)
        session.commit()
        return True
    
    @staticmethod
    def add_message_to_conversation(
        session: Session, 
        conversation_id: UUID, 
        role: str, 
        content: str,
        metadata: Optional[str] = None
    ) -> Optional[ConversationMessage]:
        """Add a message to a conversation"""
        message = ConversationMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata_json=metadata
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
    
    @staticmethod
    def get_messages_for_conversation(session: Session, conversation_id: UUID) -> List[ConversationMessage]:
        """Get all messages for a specific conversation"""
        statement = select(ConversationMessage).where(
            ConversationMessage.conversation_id == conversation_id
        ).order_by(ConversationMessage.timestamp)
        return session.exec(statement).all()
    
    @staticmethod
    def get_latest_conversation_for_user(session: Session, user_id: UUID) -> Optional[Conversation]:
        """Get the most recently updated conversation for a user"""
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc())
        result = session.exec(statement).first()
        return result