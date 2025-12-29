# Phase 1 Todo Application

A console-based todo application built with Python, following clean architecture principles and specification-driven development.

## Features

- **Add Tasks**: Create tasks with required title and optional description
- **View Tasks**: Display all tasks with ID, title, description, and completion status
- **Update Tasks**: Modify existing task title and/or description
- **Delete Tasks**: Remove tasks with confirmation prompt
- **Toggle Completion**: Mark tasks as complete/incomplete
- **In-Memory Storage**: All tasks stored in memory (no persistence)

## Requirements

- Python 3.13+

## Installation

1. Clone the repository
2. Ensure Python 3.13+ is installed
3. No additional dependencies required (uses Python standard library only)

## Usage

Run the application:
```bash
python src/main.py
```

The application will start with a menu-driven interface:

```
==================================================
                 TODO APPLICATION
==================================================
1. Add Task        - Create a new task
2. View All Tasks  - Display all tasks
3. Update Task     - Modify existing task
4. Delete Task     - Remove a task (with confirmation)
5. Toggle Complete - Mark task as complete/incomplete
6. Help            - Show instructions
7. Exit            - Quit the application
--------------------------------------------------
Instructions:
- Enter the number of your choice
- For task operations, you'll be prompted for task ID
- Empty titles are not allowed
- Use '0' to cancel operations when prompted
--------------------------------------------------
```

## Architecture

This application follows clean architecture principles:

- **Models**: Data structures and validation (src/models/)
- **Repositories**: Data access layer (src/repositories/)
- **Services**: Business logic (src/services/)
- **CLI**: User interface (src/main.py)
- **Lib**: Utilities (src/lib/)

## Validation Rules

- Task titles must be non-empty strings
- Task IDs are auto-generated and unique
- New tasks have completion status set to false by default
- All operations validate inputs before execution
- Delete operations require confirmation

## Error Handling

- Invalid inputs are handled gracefully
- Clear error messages are displayed
- Application does not crash on invalid input
- Non-existent tasks return appropriate error messages

## Testing

The application includes comprehensive test coverage:

- Unit tests for models, services, and repositories
- Integration tests for CLI workflows
- Error scenario testing

Run tests with:
```bash
python -m pytest
```

## Development

This project was developed using specification-driven development with Claude Code, following the architecture defined in the plan and specification documents.

## Compliance

This implementation strictly adheres to Phase 1 requirements and does not include any out-of-scope features such as:
- Priorities, tags, or categories
- Search or filter functionality
- Due dates or reminders
- Recurring tasks
- Web interface
- Database persistence