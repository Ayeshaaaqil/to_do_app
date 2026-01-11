from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class ConversationMessage(SQLModel, table=True):
    __tablename__ = "conversation_messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    role: str = Field(regex="^(user|assistant|system)$")  # Enum: 'user', 'assistant', 'system'
    content: str = Field(max_length=10000)
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    metadata_json: Optional[str] = Field(default=None)  # For storing additional context like OpenAI thread/run IDs


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")  # Matches the User model's table name
    title: str = Field(max_length=200)  # Generated from first message or topic
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())

    # Removed relationship to avoid circular import issues for now
    # Relationships can be handled separately if needed later