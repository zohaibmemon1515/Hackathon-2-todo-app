# Data Model: Kafka Events for Todo System

## Task Event Schema
**Purpose**: Represents task lifecycle changes for audit trails, analytics, and downstream services

**Fields**:
- `event_type`: String (task.created, task.updated, task.completed, task.deleted)
- `task_id`: String/UUID - Unique identifier of the task
- `user_id`: String/UUID - Owner of the task
- `title`: String - Task title
- `priority`: String/Enum - Task priority level (low, medium, high)
- `due_date`: DateTime - Due date for the task (nullable)
- `reminder_at`: DateTime - Reminder time (nullable)
- `tags`: Array<String> - Tags associated with the task
- `is_completed`: Boolean - Completion status
- `timestamp`: DateTime - When the event occurred

## Reminder Event Schema
**Purpose**: Contains essential information needed for reminder processing by external services

**Fields**:
- `event_type`: String (reminder.set)
- `task_id`: String/UUID - Unique identifier of the task
- `user_id`: String/UUID - Owner of the task
- `reminder_at`: DateTime - When the reminder should trigger
- `due_date`: DateTime - Due date for the task (nullable)
- `title`: String - Task title

## UI Sync Event Schema
**Purpose**: Contains minimal data needed for real-time UI updates across clients

**Fields**:
- `event_type`: String (task.sync)
- `task_id`: String/UUID - Unique identifier of the task
- `user_id`: String/UUID - Owner of the task
- `action`: String - Type of action (created, updated, completed, deleted)
- `timestamp`: DateTime - When the event occurred
- `payload`: Object - Minimal task data needed for UI updates