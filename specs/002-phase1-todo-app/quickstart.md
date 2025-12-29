# Quickstart Guide: Phase 1 Todo Application

**Feature**: Phase 1 Todo Application
**Date**: 2025-12-29
**Branch**: 002-phase1-todo-app

## Getting Started

This guide provides the essential information to understand and begin implementing the Phase 1 Todo Application.

### Prerequisites
- Python 3.13+ installed
- Console/terminal access
- [uv](https://github.com/astral-sh/uv) package manager installed
- No external runtime dependencies required (application uses Python standard library only)

### Installation with uv

The project uses uv as the package manager for development workflows:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and set up the project
git clone <repository-url>
cd <repository-name>

# Install dependencies with uv
uv sync

# Run the application
uv run python src/main.py

# Run tests
uv run python -m pytest tests/
```

### Project Structure
```
src/
├── models/
│   └── task.py          # Task domain model with validation
├── services/
│   └── task_service.py  # Business logic for task operations
├── repositories/
│   └── task_repository.py  # In-memory task storage with auto-incrementing IDs
├── cli/
│   └── todo_app.py      # Menu-driven CLI interface
└── lib/
    └── validators.py    # Input validation utilities

tests/
├── unit/
│   ├── models/
│   ├── services/
│   └── repositories/
├── integration/
│   └── cli/
└── contract/
    └── api_contracts/
```

## Key Components

### 1. Task Model (`src/models/task.py`)
- Represents the core Task entity
- Enforces validation rules (non-empty title, unique ID)
- Provides methods for state transitions (completed ↔ incomplete)

### 2. Task Repository (`src/repositories/task_repository.py`)
- Manages in-memory storage of tasks
- Handles auto-incrementing ID generation
- Provides CRUD operations for tasks

### 3. Task Service (`src/services/task_service.py`)
- Implements business logic for task operations
- Validates inputs before performing operations
- Coordinates between models and repositories

### 4. CLI Interface (`src/cli/todo_app.py`)
- Provides menu-driven console interface
- Handles user input and displays results
- Implements confirmation for destructive operations

## Implementation Steps

### Phase 1: Core Implementation
1. Implement the Task model with validation
2. Create the in-memory repository with ID management
3. Build the service layer with business logic
4. Develop the CLI interface with menu options

### Phase 2: Validation & Error Handling
1. Add comprehensive input validation
2. Implement error handling and user feedback
3. Add confirmation for delete operations
4. Test all edge cases

## Testing Strategy

### Unit Tests
- Test individual functions in each module
- Validate model validation rules
- Test repository operations
- Verify service business logic

### Integration Tests
- Test CLI interaction with service layer
- Verify end-to-end task operations
- Test error handling paths

## Key Requirements to Remember

- Console-based interface only (no web UI)
- In-memory storage only (no file/database persistence)
- No external libraries (Python standard library only)
- All Phase 1 features must be implemented
- No features beyond Phase 1 scope (as per constitution)
- Clear and readable console output required
- Graceful error handling required