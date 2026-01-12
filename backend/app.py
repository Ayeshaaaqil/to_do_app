"""
Hugging Face Space for Todo API Backend
This file creates a Gradio interface that serves as documentation for the API
"""
import gradio as gr
import subprocess
import threading
import time
import uvicorn
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import your main app
from src.main import app as fastapi_app

# Start the FastAPI app in a separate thread
def start_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

# Start FastAPI in background
thread = threading.Thread(target=start_fastapi, daemon=True)
thread.start()

# Wait for FastAPI to start
time.sleep(3)

# Create Gradio interface
with gr.Blocks(title="Todo API Backend") as app:
    gr.Markdown("# Todo API Backend with AI Assistant")
    gr.Markdown("This is the backend API for the Todo application with AI-powered task management.")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### API Documentation")
            gr.Markdown("""
            **Authentication:**
            - `POST /api/auth/signup` - Create new user
            - `POST /api/auth/signin` - Login user
            - `POST /api/auth/signout` - Logout user
            
            **Todo Management:**
            - `GET /api/todos` - Get user's todos
            - `POST /api/todos` - Create new todo
            - `PUT /api/todos/{id}` - Update todo
            - `PATCH /api/todos/{id}/complete` - Toggle completion
            - `DELETE /api/todos/{id}` - Delete todo
            
            **AI Assistant:**
            - `POST /api/chat` - Chat with AI assistant
            """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### How to Use")
            gr.Markdown("""
            1. The API is running on port 8000
            2. Make HTTP requests to the endpoints
            3. For protected endpoints, include Authorization header with Bearer token
            4. The AI assistant can process natural language requests for todo management
            """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Example API Calls")
            gr.Code("""
# Example signup request
curl -X POST http://localhost:8000/api/auth/signup \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepassword"
  }'

# Example chat request
curl -X POST http://localhost:8000/api/chat \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
  -d '{
    "message": "Add buy groceries to my todos",
    "conversation_id": null
  }'
            """)

# Launch the Gradio app
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)