# Task API Contract: Phase 1 Todo Application

**Feature**: Phase 1 Todo Application
**Date**: 2025-12-29
**Branch**: 002-phase1-todo-app

## Overview

This contract defines the interface for the task management operations in the Phase 1 Todo Application. Since this is a console-based application, these represent the internal service interfaces that will be used by the CLI layer.

## Service Interface: TaskService

### Add Task
```
Method: add_task(title: str, description: str = "") -> int
```

**Input Parameters:**
- title (str, required): Non-empty task title
- description (str, optional): Task description (default: "")

**Returns:**
- int: Unique task ID

**Validation:**
- Title must be non-empty string
- Description is optional

**Success Response:**
- Returns unique integer ID of created task
- Task status defaults to incomplete (false)

**Error Cases:**
- ValueError: If title is empty

### Get All Tasks
```
Method: get_all_tasks() -> List[Task]
```

**Input Parameters:**
- None

**Returns:**
- List[Task]: List of all tasks in the system

**Success Response:**
- Returns empty list if no tasks exist
- Returns list of Task objects with id, title, description, completed status

### Get Task by ID
```
Method: get_task_by_id(task_id: int) -> Task
```

**Input Parameters:**
- task_id (int, required): Unique task identifier

**Returns:**
- Task: Task object with id, title, description, completed status

**Error Cases:**
- ValueError: If task with given ID does not exist

### Update Task
```
Method: update_task(task_id: int, title: str = None, description: str = None) -> bool
```

**Input Parameters:**
- task_id (int, required): Unique task identifier
- title (str, optional): New task title (if provided)
- description (str, optional): New task description (if provided)

**Returns:**
- bool: True if update was successful

**Validation:**
- If title is provided, it must be non-empty
- Task with given ID must exist

**Error Cases:**
- ValueError: If task with given ID does not exist
- ValueError: If title is provided but is empty

### Delete Task
```
Method: delete_task(task_id: int) -> bool
```

**Input Parameters:**
- task_id (int, required): Unique task identifier

**Returns:**
- bool: True if deletion was successful

**Validation:**
- Task with given ID must exist

**Error Cases:**
- ValueError: If task with given ID does not exist

### Toggle Task Completion
```
Method: toggle_task_completion(task_id: int) -> bool
```

**Input Parameters:**
- task_id (int, required): Unique task identifier

**Returns:**
- bool: True if toggle was successful

**Validation:**
- Task with given ID must exist

**Success Response:**
- Toggles completed status (false → true or true → false)

**Error Cases:**
- ValueError: If task with given ID does not exist

## Data Model: Task

### Structure
```
Task {
    id: int (required, unique, auto-generated)
    title: str (required, non-empty)
    description: str (optional, default: "")
    completed: bool (required, default: false)
}
```

### Validation Rules
1. id: Must be positive integer, unique across all tasks
2. title: Must be non-empty string
3. description: Optional string
4. completed: Boolean value, defaults to false

## CLI Interface

### Menu Options
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task as Complete/Incomplete
6. Exit

### Error Handling
- All error messages must be user-friendly
- Invalid inputs handled gracefully without crashing
- Confirmation required for delete operations