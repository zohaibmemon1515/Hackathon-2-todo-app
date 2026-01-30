# Quickstart Guide: Advanced Todo Features

## Overview
This guide provides instructions for setting up and running the enhanced Todo application with advanced features including tags, search, advanced filtering, sorting, recurrence, and reminder configuration.

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (Neon serverless database)
- Poetry or uv for Python dependency management
- Docker (optional, for containerized deployment)

## Setup Instructions

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Install backend dependencies
cd apps/backend
uv sync  # or poetry install

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Database Configuration
```bash
# Set up environment variables
cp .env.example .env
# Edit .env with your database connection details
```

### 3. Database Migrations
```bash
# Run database migrations to create tables
cd apps/backend
uv run alembic upgrade head
```

### 4. Running the Application

#### Backend (API Server)
```bash
cd apps/backend
uv run python -m src.main
# API will be available at http://localhost:8000
```

#### Frontend (Web Interface)
```bash
cd apps/frontend
npm run dev
# Frontend will be available at http://localhost:3000
```

## Key Features and Usage

### 1. Enhanced Task Creation
Create tasks with advanced features using the POST `/tasks` endpoint:

```json
{
  "title": "Complete project proposal",
  "description": "Finish the project proposal document for client review",
  "due_date": "2024-12-31T17:00:00Z",
  "priority": "high",
  "tags": ["work", "important"],
  "recurrence_rule": {
    "frequency": "monthly",
    "interval": 1,
    "end_condition": {
      "type": "after_occurrences",
      "value": 12
    }
  },
  "reminder_config": {
    "offset_minutes": 60,
    "notification_method": "email"
  }
}
```

### 2. Advanced Search and Filtering
Query tasks with the enhanced GET `/tasks` endpoint:

```bash
# Search for tasks containing "project" in title or description
GET /tasks?query=project

# Filter by multiple tags
GET /tasks?tags=work&tags=important

# Filter by due date range
GET /tasks?due_date_from=2024-12-01&due_date_to=2024-12-31

# Sort by due date (ascending)
GET /tasks?sort_by=due_date&sort_order=asc

# Combine multiple filters
GET /tasks?query=meeting&tags=work&due_date_from=2024-12-01&sort_by=priority&sort_order=desc
```

### 3. Frontend Integration
The enhanced frontend components support:
- Tag input with autocomplete suggestions
- Advanced search bar with real-time filtering
- Sort controls for different criteria
- Form fields for recurrence and reminder configuration
- Filter sidebar with tag and date range selectors

## Development Workflow

### Adding New Advanced Features
1. Update the data model in `apps/backend/src/models/task.py`
2. Extend the schema in `apps/backend/src/schemas/task.py`
3. Modify the service layer in `apps/backend/src/services/task_service.py`
4. Update the API endpoints in `apps/backend/src/api/tasks.py`
5. Extend frontend components in `apps/frontend/src/components/tasks/`

### Database Migrations
```bash
# Generate a new migration
alembic revision --autogenerate -m "Add advanced features to task model"

# Apply the migration
alembic upgrade head
```

## Testing
Run the complete test suite to verify functionality:

```bash
# Backend tests
cd apps/backend
uv run pytest

# Frontend tests
cd apps/frontend
npm test
```

## Deployment
The application is configured for deployment with the Helm chart located in `apps/helm/todo-app/`. Use the following commands for Kubernetes deployment:

```bash
# Package and deploy with Helm
helm install todo-app apps/helm/todo-app --values apps/helm/todo-app/values.yaml
```

## Troubleshooting
- Ensure database migrations are applied before starting the backend
- Check that environment variables are properly configured
- Verify that both frontend and backend are running for full functionality
- Monitor logs for any errors during startup or operation