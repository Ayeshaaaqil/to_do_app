# Todo API Backend with AI Assistant

This is a backend API for a Todo application with AI-powered task management capabilities. The API is built with FastAPI and includes authentication, todo management, and an AI assistant that understands natural language commands.

## Features

- **User Authentication**: Secure signup and signin with JWT tokens
- **Todo Management**: Full CRUD operations for managing tasks
- **AI Assistant**: Natural language processing for todo management
- **Database Integration**: PostgreSQL/Neon database with SQLModel ORM
- **Real-time Chat**: Interactive chat interface for AI assistant

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/signin` - Login user
- `POST /api/auth/signout` - Logout user

### Todo Management
- `GET /api/todos` - Get user's todos
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo
- `PATCH /api/todos/{id}/complete` - Toggle completion
- `DELETE /api/todos/{id}` - Delete todo

### AI Assistant
- `POST /api/chat` - Chat with AI assistant

## Deployment to Hugging Face Spaces

This application is designed to be deployed on Hugging Face Spaces using the Gradio framework. The application will automatically create a public URL that exposes the FastAPI backend.

## Usage

Once deployed, you can access the API endpoints using the public URL provided by Hugging Face Spaces. The AI assistant can process natural language commands like:
- "Add 'buy groceries' to my todos"
- "Show me my todos"
- "Update 'buy groceries' to 'buy groceries and milk'"
- "Mark 'buy groceries' as complete"
- "Delete 'buy groceries'"

## Technologies Used

- FastAPI: High-performance web framework
- SQLModel: SQL database modeling
- Pydantic: Data validation
- Gradio: Interface for Hugging Face Spaces
- Neon: Cloud PostgreSQL database
- JWT: Authentication tokens
- OpenAI: AI assistant capabilities