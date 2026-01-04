# Phase II Todo Web Application

This is the Phase II implementation of the "Evolution of Todo" project - a full-stack web application with user authentication and todo management features.

## Features

- User authentication (signup/signin)
- Todo management (create, read, update, delete)
- Mark todos as complete/incomplete
- User-specific data isolation
- Responsive UI for desktop and mobile

## Tech Stack

### Backend
- Python 3.13+
- FastAPI
- SQLModel
- Neon PostgreSQL
- JWT for authentication

### Frontend
- Next.js 14+
- TypeScript
- Tailwind CSS

## Setup

### Backend
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (see `.env.example`)
6. Run the application: `uvicorn src.main:app --reload`

### Frontend
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install` or `yarn install`
3. Set up environment variables (see `.env.local.example`)
4. Run the development server: `npm run dev` or `yarn dev`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create a new user
- `POST /api/auth/signin` - Authenticate a user
- `POST /api/auth/signout` - Sign out a user

### Todos
- `GET /api/todos` - Get all todos for the authenticated user
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `PATCH /api/todos/{id}/complete` - Toggle todo completion status
- `DELETE /api/todos/{id}` - Delete a specific todo

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running Tests

Backend tests: `pytest`

Frontend tests: `npm run test` or `yarn test`# to_do_app
