from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Todo API Test", version="0.1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API - Test"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)