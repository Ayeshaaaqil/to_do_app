# Quickstart Guide: Phase II Todo Web Application

## Prerequisites

- Python 3.13+
- Node.js 18+ and npm/yarn
- Neon PostgreSQL account and database
- Better Auth account (or local setup)

## Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   # or
   yarn install
   ```

## Configuration

1. Create `.env` files in both backend and frontend directories:

   **Backend (.env)**:
   ```
   DATABASE_URL=postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname
   SECRET_KEY=your-secret-key-here
   ```

   **Frontend (.env.local)**:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## Running the Application

1. Start the backend:
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   # or
   yarn dev
   ```

3. Access the application at `http://localhost:3000`

## API Documentation

The backend API documentation is available at `http://localhost:8000/docs` when running in development mode.

## Testing

1. Backend tests:
   ```bash
   cd backend
   pytest
   ```

2. Frontend tests:
   ```bash
   cd frontend
   npm run test
   # or
   yarn test
   ```

## Deployment

1. Backend deployment:
   - Deploy to a Python-compatible platform (e.g., Heroku, Railway, Vercel, etc.)
   - Ensure environment variables are set
   - Run migrations in the deployment environment

2. Frontend deployment:
   - Build the application: `npm run build` or `yarn build`
   - Deploy the build output to a static hosting service (Vercel, Netlify, etc.)
   - Ensure environment variables are set for the deployed environment