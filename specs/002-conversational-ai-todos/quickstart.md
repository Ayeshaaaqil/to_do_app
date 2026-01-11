# Quickstart Guide: Conversational AI Todo Management

## Overview
This guide provides instructions for setting up and running the conversational AI todo management feature locally.

## Prerequisites
- Python 3.13+
- Poetry or pip for dependency management
- Access to OpenAI API (with Assistant API enabled)
- Access to MCP server
- PostgreSQL database (Neon recommended)
- Node.js 18+ (for frontend, if needed)

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or if using poetry
poetry install
```

### 3. Environment Variables
Create a `.env` file in the backend directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
ASSISTANT_ID=your_assistant_id_here  # Created via OpenAI API

# MCP Server Configuration
MCP_SERVER_URL=http://localhost:8001
MCP_CLIENT_TIMEOUT=30

# Authentication
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Other configurations
DEBUG=true
LOG_LEVEL=INFO
```

## Running the Application

### 1. Database Setup
```bash
# Run database migrations
python -m alembic upgrade head
```

### 2. Start the MCP Server
```bash
# In a separate terminal
cd backend/src/mcp
python mcp_server.py
```

### 3. Start the Main Application
```bash
# From the backend directory
uvicorn src.main:app --reload --port 8000
```

## Key Components

### 1. Chat API Endpoint
Located in `backend/src/api/chat.py`
- Handles user requests to the conversational AI
- Manages authentication and conversation state
- Orchestrates communication between AI agent and MCP tools

### 2. AI Agent Implementation
Located in `backend/src/agents/todo_agent.py`
- Implements the OpenAI Assistant API integration
- Processes natural language input
- Determines appropriate MCP tool to invoke

### 3. MCP Server and Tools
Located in `backend/src/mcp/`
- Implements the Model Context Protocol server
- Defines MCP tools for todo operations (create, read, update, delete, mark complete)
- Handles database interactions

### 4. Data Models
Located in `backend/src/models/`
- Extended from Phase II models
- Includes Conversation and ConversationMessage models
- Maintains relationships between users, todos, and conversations

## Testing

### Unit Tests
```bash
# Run all tests
pytest

# Run tests for specific module
pytest tests/unit/test_chat_api.py

# Run tests with coverage
pytest --cov=src
```

### Integration Tests
```bash
# Run integration tests
pytest tests/integration/
```

## Development Workflow

### 1. Creating New MCP Tools
1. Define the tool in `backend/src/mcp/tools/`
2. Register the tool with the MCP server
3. Add corresponding function to the AI agent's tool list
4. Write unit tests for the new tool

### 2. Modifying the AI Agent
1. Update the agent's instructions in `backend/src/agents/todo_agent.py`
2. Adjust the tools available to the agent
3. Test the agent's behavior with various inputs
4. Update integration tests as needed

### 3. Updating Data Models
1. Modify the model definitions in `backend/src/models/`
2. Create a new migration using Alembic
3. Test the migration in a development database
4. Update any affected services or endpoints

## Troubleshooting

### Common Issues

1. **OpenAI API Connection Errors**
   - Verify your API key is correct
   - Check that the Assistant ID is valid
   - Ensure you have access to the OpenAI Assistant API

2. **MCP Server Connection Errors**
   - Verify the MCP server is running
   - Check that the URL in environment variables is correct
   - Ensure the MCP server has proper database connectivity

3. **Authentication Failures**
   - Verify your JWT token is valid and not expired
   - Check that the secret key matches between frontend and backend

### Debugging Tips

1. Enable debug logging by setting `DEBUG=true` in your environment
2. Use the conversation ID to trace requests through the system
3. Check the database directly to verify data persistence
4. Monitor the MCP server logs for tool invocation details