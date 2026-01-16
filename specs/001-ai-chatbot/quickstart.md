# Quickstart Guide: AI Powered Todo Chatbot

## Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed (for frontend)
- PostgreSQL database (or Neon account)
- OpenAI API key

## Setup Steps

### 1. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd apps/backend

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python -m src.database.migrate
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd apps/frontend

# Install dependencies
npm install
```

### 4. Running the Application
```bash
# Start backend
cd apps/backend
python -m src.main

# In a separate terminal, start frontend
cd apps/frontend
npm run dev
```

## Key Endpoints
- Chat API: `POST /api/{user_id}/chat`
- Conversations: `GET /api/conversations`
- Messages: `GET /api/conversations/{conversation_id}/messages`

## Testing the Chatbot
1. Navigate to the chat interface in your browser
2. Authenticate as a user
3. Start a conversation by typing "Add a task to buy groceries"
4. The AI should respond with confirmation and create the task

## Development Commands
```bash
# Run backend tests
cd apps/backend && pytest

# Run frontend tests
cd apps/frontend && npm test

# Lint code
cd apps/backend && flake8 src/
cd apps/frontend && npm run lint
```