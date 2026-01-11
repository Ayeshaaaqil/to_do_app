# Data Model: Conversational AI Todo Management

## Overview
This document defines the data models for the conversational AI todo management feature, extending the existing Phase II models.

## Entity Definitions

### User (Extended from Phase II)
**Description**: Represents an authenticated user with associated todos and conversations
**Fields**:
- id: Integer (Primary Key)
- email: String (Unique, Indexed)
- hashed_password: String
- created_at: DateTime
- updated_at: DateTime

### Todo (Extended from Phase II)
**Description**: Represents a user's todo item with properties like title, description, completion status, and creation/modification timestamps
**Fields**:
- id: Integer (Primary Key)
- title: String (Indexed)
- description: String (Optional)
- completed: Boolean (Default: False)
- user_id: Integer (Foreign Key to User.id)
- created_at: DateTime
- updated_at: DateTime

### Conversation
**Description**: Represents a user's conversation with the AI assistant, including message history and context
**Fields**:
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key to User.id)
- title: String (Generated from first message or topic)
- created_at: DateTime
- updated_at: DateTime

### ConversationMessage
**Description**: Represents individual messages within a conversation
**Fields**:
- id: Integer (Primary Key)
- conversation_id: Integer (Foreign Key to Conversation.id)
- role: String (Enum: 'user', 'assistant', 'system')
- content: Text
- timestamp: DateTime
- metadata: JSON (For storing additional context like OpenAI thread/run IDs)

## Relationships

### User ↔ Todo
- One-to-Many relationship
- User.id → Todo.user_id
- Cascading delete: When a user is deleted, their todos are also deleted

### User ↔ Conversation
- One-to-Many relationship
- User.id → Conversation.user_id
- Cascading delete: When a user is deleted, their conversations are also deleted

### Conversation ↔ ConversationMessage
- One-to-Many relationship
- Conversation.id → ConversationMessage.conversation_id
- Cascading delete: When a conversation is deleted, its messages are also deleted

## Validation Rules

### Todo Validation
- Title must be between 1 and 200 characters
- Description must be between 0 and 1000 characters if provided
- User ID must reference an existing user
- Completed status must be boolean

### Conversation Validation
- Title must be between 1 and 200 characters
- User ID must reference an existing user

### ConversationMessage Validation
- Role must be one of 'user', 'assistant', or 'system'
- Content must be between 1 and 10000 characters
- Conversation ID must reference an existing conversation
- Timestamp must be in the past or present

## State Transitions

### Todo State Transitions
- `incomplete` → `complete`: When user marks todo as complete
- `complete` → `incomplete`: When user marks todo as incomplete

### Conversation State Transitions
- `created` → `active`: When first user message is received
- `active` → `paused`: When conversation is inactive for extended periods (optional feature)
- `paused` → `active`: When user resumes conversation

## Indexes

### Todo Indexes
- idx_todo_user_id: Index on user_id for efficient user todo queries
- idx_todo_completed: Index on completed for efficient filtering
- idx_todo_created_at: Index on created_at for chronological ordering

### Conversation Indexes
- idx_conversation_user_id: Index on user_id for efficient user conversation queries
- idx_conversation_updated_at: Index on updated_at for chronological ordering

### ConversationMessage Indexes
- idx_message_conversation_id: Index on conversation_id for efficient conversation message queries
- idx_message_timestamp: Index on timestamp for chronological ordering