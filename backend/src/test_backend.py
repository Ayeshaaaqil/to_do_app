import requests
import time
import threading
from main import app
import uvicorn

def run_server():
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level="info")

if __name__ == "__main__":
    # Start server in a thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    print("Server started, waiting for it to be ready...")
    time.sleep(3)  # Wait for server to start
    
    try:
        # Test the health endpoint
        response = requests.get('http://127.0.0.1:8000/health')
        print(f'Health check status: {response.status_code}')
        print(f'Health check response: {response.json()}')
        
        # Test the root endpoint
        response = requests.get('http://127.0.0.1:8000/')
        print(f'Root endpoint status: {response.status_code}')
        print(f'Root endpoint response: {response.json()}')
        
        # Test the todos endpoint
        response = requests.get('http://127.0.0.1:8000/api/todos')
        print(f'Todos endpoint status: {response.status_code}')
        print(f'Todos endpoint response: {response.json()}')
        
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Make sure it's running on http://127.0.0.1:8000")
    except Exception as e:
        print(f'Error during testing: {e}')
    
    input("Press Enter to stop the server...")