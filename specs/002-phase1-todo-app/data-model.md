# Data Model: Phase 1 Todo Application

**Feature**: Phase 1 Todo Application
**Date**: 2025-12-29
**Branch**: 002-phase1-todo-app

## Task Entity

### Attributes

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| id | integer | Yes | Auto-generated | Unique, positive integer |
| title | string | Yes | N/A | Non-empty, string |
| description | string | No | Empty string | Optional, string |
| completed | boolean | Yes | false | Boolean value |

### Relationships
- No relationships with other entities (standalone entity)

### State Transitions
- completed: false ↔ true (toggle operation)

### Business Rules
1. Title must be non-empty string
2. ID must be unique across all tasks
3. ID is auto-generated on creation
4. New tasks have completed status set to false by default

## TaskList Collection

### Attributes
- tasks: List of Task entities
- next_id: Integer counter for auto-incrementing IDs

### Operations
1. add_task(task) - Add a new task to the collection
2. get_all_tasks() - Retrieve all tasks
3. get_task_by_id(task_id) - Retrieve specific task
4. update_task(task_id, updates) - Update specific task fields
5. delete_task(task_id) - Remove task from collection
6. toggle_task_completion(task_id) - Toggle completed status

### Validation Rules
1. Task IDs must exist when performing operations
2. Title validation must pass before adding/updating tasks
3. Only existing fields (title, description, completed) can be updated
4. Delete operations require confirmation before execution

## Domain Constraints

### From Functional Requirements
- **FR-001**: Task creation requires title, description is optional
- **FR-002**: System auto-generates unique integer IDs
- **FR-003**: Default status for new tasks is incomplete (false)
- **FR-008**: Task titles must be non-empty strings
- **FR-011**: Tasks with empty titles are rejected
- **FR-012**: Only existing fields (title, description, completed) can be updated
- **FR-015**: Task IDs must remain unique

### Validation Implementation
- Task creation: Validate title is non-empty before creating
- Task updates: Validate title is non-empty if provided
- Task retrieval: Validate task ID exists before operations
- ID generation: Use auto-incrementing counter to ensure uniqueness