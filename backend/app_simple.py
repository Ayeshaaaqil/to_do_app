"""
Hugging Face Space for Todo API Backend
This file creates a Gradio interface that hosts the FastAPI backend
"""
import os
import subprocess
import threading
import time
import requests
import gradio as gr
from pyngrok import ngrok
import atexit
import uvicorn
import sys
from threading import Event

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import your main app
from src.main import app as fastapi_app

# Global variable to store the public URL
public_url = None

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
        gr.Markdown("### Test API Health")
        def test_health():
            try:
                # On Hugging Face Spaces, the API is available at the same domain
                response = requests.get("http://localhost:8000/health")
                if response.status_code == 200:
                    return "✅ API is healthy", "Healthy"
                else:
                    return f"❌ API returned status {response.status_code}", "Error"
            except Exception as e:
                return f"❌ Error connecting to API: {str(e)}", "Error"
        
        health_btn = gr.Button("Test API Health")
        health_result = gr.Textbox(label="Result")
        
        health_btn.click(test_health, outputs=[health_result])

# Launch the Gradio app
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)