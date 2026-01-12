# Deployment Guide for Hugging Face Space

This guide explains how to deploy your Todo API backend to your Hugging Face Space at: https://huggingface.co/spaces/Ayesha-Aaqil/hackaton-2

## Step-by-Step Deployment

### 1. Clone Your Space Repository
```bash
git clone https://huggingface.co/spaces/Ayesha-Aaqil/hackaton-2
cd hackaton-2
```

### 2. Copy Backend Files
Copy all the backend files from your project to the space repository:

```bash
# From your project directory, copy the necessary files
cp -r C:/Users/Dell/Desktop/phase2/backend/src .
cp C:/Users/Dell/Desktop/phase2/backend/app.py .
cp C:/Users/Dell/Desktop/phase2/backend/requirements_hf.txt requirements.txt
cp C:/Users/Dell/Desktop/phase2/backend/.env.example .env  # Create a .env file with your environment variables
cp C:/Users/Dell/Desktop/phase2/backend/README.md .
```

### 3. Create Environment File
Create a `.env` file with your environment variables:

```env
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
NEON_DATABASE_URL=your-neon-database-url
OPENAI_API_KEY=your-openai-api-key-if-using
```

### 4. Update requirements.txt
Make sure your `requirements.txt` contains:

```
fastapi==0.104.1
sqlmodel==0.0.16
pydantic==2.5.0
uvicorn==0.24.0
psycopg2-binary==2.9.9
python-multipart==0.0.6
python-dotenv==1.0.0
asyncpg==0.29.0
passlib==1.7.4
bcrypt==4.0.1
pyjwt==2.8.0
gradio==4.12.0
requests==2.31.0
torch==2.1.2
transformers==4.36.0
accelerate==0.25.0
```

### 5. Commit and Push Changes
```bash
git add .
git commit -m "Add Todo API backend"
git push origin main
```

### 6. Configure Space Settings (Optional)
If needed, go to your Space settings on Hugging Face and:
- Set the hardware tier (CPU Standard is usually sufficient)
- Add secrets/environment variables in the "Files" tab under "Secrets"

## Alternative Method: Direct Upload

If you prefer to upload files directly:
1. Go to https://huggingface.co/spaces/Ayesha-Aaqil/hackaton-2/settings
2. Click on "Files" tab
3. Upload the following files:
   - `src/` directory (containing your backend code)
   - `app.py` (the Gradio interface)
   - `requirements.txt`
   - `README.md`
   - `.env` (with your environment variables)

## API Usage After Deployment

Once deployed, your API will be accessible at:
`https://ayesha-aaqil-hackaton-2.hf.space`

API endpoints:
- `POST https://ayesha-aaqil-hackaton-2.hf.space/api/auth/signup`
- `POST https://ayesha-aaqil-hackaton-2.hf.space/api/chat`
- `GET https://ayesha-aaqil-hackaton-2.hf.space/api/todos`
- And all other endpoints with the same path structure

## Troubleshooting

If you encounter issues:
1. Check the Space logs in the "Logs" tab
2. Ensure all dependencies are listed in requirements.txt
3. Verify environment variables are properly set
4. Make sure the app.py file starts both FastAPI and Gradio servers

## Features

Your deployed API includes:
- User authentication (signup/signin)
- Todo management (CRUD operations)
- AI assistant for natural language processing
- Secure JWT-based authentication
- Database integration