# Research: Conversational AI Todo Management

## Overview
This document captures research findings and technical decisions for implementing the conversational AI todo management feature in Phase III of the Evolution of Todo project.

## AI & Agent Implementation

### Decision: OpenAI Assistant API for AI Agent Functionality
**Rationale**: The OpenAI Assistant API provides a robust framework for creating AI agents that can understand natural language and execute tools. It integrates well with the MCP protocol and allows for persistent thread-based conversations.

**Alternatives considered**:
- Custom LLM implementation: Would require significant development effort and maintenance
- LangChain agents: More complex for this specific use case
- Anthropic Claude: Would require different integration patterns

### Decision: Agent Responsibilities
**Rationale**: The AI agent will be responsible for:
- Processing natural language input from users
- Determining user intent (create, read, update, delete, mark complete/incomplete)
- Identifying relevant parameters (todo title, description, etc.)
- Invoking appropriate MCP tools to perform operations
- Formulating natural language responses based on tool results

### Decision: Tool Selection and Invocation Strategy
**Rationale**: The agent will use a function-calling approach where each todo operation is exposed as a distinct tool. The agent will analyze the user's natural language input and select the appropriate tool based on intent detection.

**Tools to be implemented**:
- create_todo(title: str, description: str) -> Todo
- get_todos() -> List[Todo]
- update_todo(todo_id: int, title: str, description: str) -> Todo
- delete_todo(todo_id: int) -> bool
- toggle_todo_completion(todo_id: int, complete: bool) -> Todo

### Decision: Agent Lifecycle Per Request
**Rationale**: For statelessness and scalability, each chat request will instantiate a new agent run. The conversation context will be maintained by the thread in the OpenAI API and the conversation state stored in our database.

## MCP Server Implementation

### Decision: Official MCP SDK for MCP Server
**Rationale**: Using the official Model Context Protocol SDK ensures compliance with the MCP standard and provides built-in functionality for tool discovery and invocation.

### Decision: MCP Server Responsibilities
**Rationale**: The MCP server will:
- Expose todo operations as standardized tools
- Handle authentication and authorization for each tool call
- Interact with the database to perform operations
- Return structured results to the AI agent

### Decision: Stateless MCP Tools for Todo Operations
**Rationale**: Each MCP tool will be stateless and receive all necessary context (user ID, parameters) as input. This ensures scalability and reliability.

### Decision: Database Interaction via MCP Tools
**Rationale**: All database operations will be performed within the MCP tools to maintain the constraint that tools handle data persistence. This also centralizes data access logic.

### Decision: Error Propagation from MCP Tools to Agent
**Rationale**: MCP tools will return structured error responses that the AI agent can interpret and translate into user-friendly messages.

## Chat API Implementation

### Decision: Stateless Chat Endpoint Structure
**Rationale**: The chat endpoint will be stateless, retrieving conversation context from the database and passing it to the AI agent. This ensures scalability and fault tolerance.

### Decision: Conversation Context Retrieval and Persistence
**Rationale**: The chat API will retrieve the user's conversation history from the database and store new messages after processing. This maintains conversation continuity across requests.

### Decision: Authentication Enforcement
**Rationale**: The chat API will enforce authentication using the existing Better Auth middleware before processing any requests.

### Decision: Request/Response Lifecycle
**Rationale**: The lifecycle will be:
1. Authenticate user
2. Retrieve conversation history from database
3. Send user message and history to AI agent
4. Agent invokes MCP tools as needed
5. Receive response from agent
6. Store new messages in conversation history
7. Return response to user

## Data Implementation

### Decision: Conversation Data Model
**Rationale**: The conversation entity will store:
- User ID (foreign key to user)
- Conversation metadata
- Message history (serialized or in separate messages table)
- Timestamps

### Decision: Relationship Between Users, Conversations, and Todos
**Rationale**: 
- Users have many conversations
- Users have many todos
- Conversations contain messages that relate to specific todos
- Foreign keys will ensure data integrity

### Decision: Persistence Strategy
**Rationale**: All data will be persisted in the Neon Serverless PostgreSQL database using SQLModel, consistent with Phase II implementation.

## Integration Implementation

### Decision: Chat API ↔ Agent Interaction
**Rationale**: The chat API will create a thread in the OpenAI API and run the assistant, passing the user's message and any required context.

### Decision: Agent ↔ MCP Tool Interaction
**Rationale**: The agent will call MCP tools through the MCP server when it determines that a todo operation is needed based on user intent.

### Decision: MCP ↔ Database Interaction
**Rationale**: MCP tools will connect directly to the PostgreSQL database to perform CRUD operations on todos and conversations, using the same connection pool as the rest of the application.

## Constraints Compliance

### Decision: No UI Changes
**Rationale**: The conversational AI functionality will be exposed through the existing chat API endpoint, requiring no frontend modifications.

### Decision: No Autonomous Agents
**Rationale**: Agents will only run in response to user-initiated requests, not autonomously in the background.

### Decision: No Memory Stored Outside Database
**Rationale**: All state will be persisted in the database, with the exception of temporary in-memory processing during a single request.

### Decision: No Future Phase Infrastructure
**Rationale**: Implementation will strictly adhere to Phase III requirements without adding infrastructure for future phases.