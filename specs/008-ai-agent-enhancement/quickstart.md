# Quickstart Guide: AI Agent Enhancement

## Overview
Quick setup guide for implementing the AI Agent Enhancement feature with new commands and Urdu support while maintaining compatibility with existing infrastructure.

## Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed
- Docker and Docker Compose installed
- OpenAI API key
- MCP (Model Context Protocol) server configured
- Existing backend services running (PostgreSQL, Kafka)

## Environment Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-root>
```

### 2. Backend Setup
```bash
cd apps/backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenAI API key and other configurations
```

### 3. Frontend Setup
```bash
cd apps/frontend
npm install
cp .env.example .env.local
# Edit .env.local as needed
```

## Running the Application

### 1. Start Infrastructure
```bash
# From repository root
docker-compose up -d postgres kafka zookeeper
```

### 2. Initialize Database
```bash
cd apps/backend
python create_tables.py
```

### 3. Start Backend Services
```bash
# Terminal 1: Start MCP server
cd apps/backend
python -m src/mcp/server.py

# Terminal 2: Start main backend
cd apps/backend
uvicorn src/main:app --reload --port 8000
```

### 4. Start Frontend
```bash
cd apps/frontend
npm run dev
```

## Key Components

### 1. Enhanced Agent Service
Located at `apps/backend/src/services/agent_service.py`
- Extends existing AI agent with new command patterns
- Integrates with existing tool chains
- Handles Roman Urdu command preprocessing

### 2. Command Mapping
Located at `apps/backend/src/services/agent_service.py`
- Maps new English commands to existing agent flows
- Translates Roman Urdu commands to English equivalents
- Maintains consistency with existing create → schedule → notify sequences

### 3. Enhanced Chat API
Located at `apps/backend/src/api/chat.py`
- Updated endpoints for new command processing
- Maintains backward compatibility
- Adds language detection and processing capabilities

## Testing the Enhanced Feature

### 1. New English Commands
Try these new sample commands in the chat interface:
- "Check pending tasks" - Retrieves and displays your pending tasks
- "Remind me tomorrow at 9am to call John" - Creates a reminder for tomorrow at 9am

### 2. Urdu Support
Try these Roman Urdu commands:
- "kal subah 9 bajay pending kaam check karen" - Check pending tasks for tomorrow morning at 9
- "kal 9 bajay mujhe yaad dilao" - Set a reminder for tomorrow at 9

### 3. Multi-step Operations
Issue complex commands that trigger existing sequences:
- "Create a task to buy groceries and remind me at 6pm today"
- "Add a high priority task and notify my team via email"

## Configuration

### OpenAI Settings
In `apps/backend/.env`:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4-turbo  # Recommended for tool calling
```

### MCP Configuration
In `apps/backend/src/config/mcp_config.py`:
```python
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 8080
MCP_TIMEOUT = 30  # seconds
```

### Language Processing Settings
Adjust language detection and processing settings:
```python
LANGUAGE_DETECTION_THRESHOLD = 0.7  # Minimum confidence for language detection
URDU_TRANSLATION_ENABLED = True     # Enable Roman Urdu support
SUPPORTED_LANGUAGES = ["en", "ur"]  # Languages supported by the system
```

## Development Workflow

### Adding New Command Patterns
1. Define the new command pattern in `agent_service.py`
2. Map the pattern to existing agent flows and tools
3. Test with various phrasings of the command
4. Update documentation

### Extending Multi-step Sequences
1. Identify the sequence of operations needed
2. Use existing MCP tools for each step
3. Ensure the sequence follows the create → schedule → notify pattern
4. Implement error handling for partial failures

## Troubleshooting

### Common Issues
- **API Key Errors**: Verify OPENAI_API_KEY is set correctly
- **MCP Connection Issues**: Ensure MCP server is running
- **Language Detection**: Check if Urdu preprocessing is working
- **Context Loss**: Verify database connectivity for conversation storage

### Debugging Enhanced AI Responses
Enable debug logging in `apps/backend/.env`:
```
LOG_LEVEL=DEBUG
AI_DEBUG_MODE=true
LANGUAGE_DEBUG_MODE=true
```

### Performance Monitoring
Monitor response times for enhanced operations:
- New command processing: <2 seconds
- Urdu command translation: <500ms
- Multi-step sequence execution: <3 seconds
- Overall response time: <3 seconds