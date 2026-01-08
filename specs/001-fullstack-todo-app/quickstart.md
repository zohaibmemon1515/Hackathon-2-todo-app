# Quickstart Guide: Full-Stack Todo Web Application (Phase-II)

**Feature**: 001-fullstack-todo-app
**Date**: 2026-01-04

## Overview

This guide provides step-by-step instructions to set up the development environment for the Full-Stack Todo Web Application with Next.js frontend, FastAPI backend, and PostgreSQL database.

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL (or access to Neon PostgreSQL)
- Git
- Docker (optional, for containerized development)

## Environment Setup

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup (FastAPI)

#### Navigate to backend directory
```bash
cd apps/backend
```

#### Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Set up environment variables
Create `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
JWT_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
NEON_DATABASE_URL=your-neon-database-url
```

#### Run database migrations
```bash
# Using Alembic
alembic upgrade head
```

#### Start the backend server
```bash
uvicorn src.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup (Next.js)

#### Navigate to frontend directory
```bash
cd apps/frontend
```

#### Install dependencies
```bash
npm install
# or
yarn install
```

#### Set up environment variables
Create `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-super-secret-jwt-key-here
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
```

#### Start the frontend development server
```bash
npm run dev
# or
yarn dev
```

Frontend will be available at `http://localhost:3000`

## Better Auth Configuration

### 1. Install Better Auth dependencies
In the frontend directory:
```bash
npm install @better-auth/react @better-auth/client
```

### 2. Configure Better Auth
Create authentication configuration in the frontend to work with the backend JWT system.

## Database Setup

### Option 1: Local PostgreSQL
1. Install PostgreSQL locally
2. Create database: `CREATE DATABASE todo_app;`
3. Update DATABASE_URL in backend `.env` file

### Option 2: Neon PostgreSQL
1. Create account at [neon.tech](https://neon.tech)
2. Create a new project
3. Update NEON_DATABASE_URL in backend `.env` file

## Running the Application

### Development Mode
1. Start backend: `cd apps/backend && uvicorn src.main:app --reload --port 8000`
2. Start frontend: `cd apps/frontend && npm run dev`
3. Access frontend at `http://localhost:3000`

### Production Mode
1. Build frontend: `cd apps/frontend && npm run build`
2. Start backend: `cd apps/backend && uvicorn src.main:app --host 0.0.0.0 --port 8000`

## Testing

### Backend Tests
```bash
cd apps/backend
python -m pytest
```

### Frontend Tests
```bash
cd apps/frontend
npm run test
```

## Common Commands

| Command | Description |
|---------|-------------|
| `cd apps/backend && uvicorn src.main:app --reload` | Start backend development server |
| `cd apps/frontend && npm run dev` | Start frontend development server |
| `cd apps/backend && python -m pytest` | Run backend tests |
| `cd apps/frontend && npm run test` | Run frontend tests |
| `cd apps/backend && alembic upgrade head` | Run database migrations |

## Troubleshooting

### Backend Issues
- If getting database connection errors, verify PostgreSQL is running and credentials are correct
- If getting JWT errors, ensure JWT_SECRET is the same in both frontend and backend

### Frontend Issues
- If API calls are failing, ensure NEXT_PUBLIC_API_BASE_URL points to the correct backend URL
- If authentication isn't working, check that Better Auth is properly configured

## Next Steps

1. Review the data models in `specs/001-fullstack-todo-app/data-model.md`
2. Examine the API contracts in `specs/001-fullstack-todo-app/contracts/`
3. Check the implementation plan in `specs/001-fullstack-todo-app/plan.md`
4. Begin with user authentication functionality
5. Implement task management features