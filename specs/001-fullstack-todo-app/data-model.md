# Data Model: Full-Stack Todo Web Application (Phase-II)

**Feature**: 001-fullstack-todo-app
**Date**: 2026-01-04
**Model Version**: 1.0

## Overview

This document defines the data models for the Full-Stack Todo Web Application, including entities, relationships, validation rules, and state transitions. The models are designed to support multi-user task isolation with secure authentication.

## Entity Definitions

### 1. User Entity

**Description**: Represents a registered user in the system

**Fields**:
- `id` (UUID/Integer): Unique identifier for the user (Primary Key)
- `email` (String): User's email address (Required, Unique, Validated)
- `hashed_password` (String): Bcrypt hashed password (Required, Secure)
- `first_name` (String): User's first name (Optional)
- `last_name` (String): User's last name (Optional)
- `is_active` (Boolean): Whether the account is active (Default: true)
- `created_at` (DateTime): Account creation timestamp (Auto-generated)
- `updated_at` (DateTime): Last update timestamp (Auto-updated)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet security requirements (length, complexity)
- Email cannot be changed after account creation

**Relationships**:
- One-to-Many: User has many Tasks

### 2. Task Entity

**Description**: Represents a personal task owned by a specific user

**Fields**:
- `id` (UUID/Integer): Unique identifier for the task (Primary Key)
- `title` (String): Task title/description (Required, Max 255 chars)
- `description` (Text): Detailed task description (Optional, Max 1000 chars)
- `is_completed` (Boolean): Whether the task is completed (Default: false)
- `created_at` (DateTime): Task creation timestamp (Auto-generated)
- `updated_at` (DateTime): Last update timestamp (Auto-updated)
- `due_date` (DateTime): Optional due date for the task (Optional)
- `priority` (String): Task priority level (Optional: 'low', 'medium', 'high')
- `user_id` (UUID/Integer): Foreign key to User (Required, References User.id)

**Validation Rules**:
- Title must be provided and not empty
- Title must be less than 255 characters
- User_id must reference an existing, active user
- Description, if provided, must be less than 1000 characters
- Due date, if provided, must be in the future

**Relationships**:
- Many-to-One: Task belongs to one User (via user_id foreign key)

## Data Relationships

### User-Task Relationship
- **Type**: One-to-Many
- **Description**: One user can have multiple tasks
- **Enforcement**: Foreign key constraint on Task.user_id referencing User.id
- **Behavior**: Tasks are not deleted when user is deleted (to be determined - either cascade delete or prevent user deletion)

## State Transitions

### Task State Transitions
- **Incomplete → Complete**: When user marks task as done
- **Complete → Incomplete**: When user unmarks completed task
- **Creation**: Task starts as incomplete when created
- **Update**: Task details can be modified while preserving ownership

### User State Transitions
- **Inactive → Active**: When account is activated (initial state)
- **Active → Inactive**: When account is deactivated (soft delete approach)

## Data Access Patterns

### Security Constraints
- **Multi-user Isolation**: Users can only access tasks where user_id matches their own user ID
- **Authentication Required**: All data access requires valid JWT authentication
- **Authorization**: Access control enforced at API layer based on JWT user ID

### Query Patterns
- **User's Tasks**: SELECT * FROM tasks WHERE user_id = [authenticated_user_id]
- **Single Task**: SELECT * FROM tasks WHERE id = [task_id] AND user_id = [authenticated_user_id]
- **Task Creation**: INSERT INTO tasks (...) VALUES (...) WHERE user_id = [authenticated_user_id]

## Validation Requirements

### Input Validation
- All inputs must be sanitized to prevent injection attacks
- Email validation follows RFC 5322 standards
- Passwords must meet minimum security requirements
- Task titles and descriptions must be properly escaped

### Business Logic Validation
- Users can only modify their own tasks
- Completed tasks can be unmarked but maintain history
- Due dates cannot be in the past (optional validation)
- Priority values must be from predefined set

## Indexing Strategy

### Required Indexes
- `users.email`: For authentication lookups (Unique)
- `tasks.user_id`: For user-specific task queries
- `tasks.created_at`: For chronological task ordering
- `tasks.is_completed`: For filtering completed tasks

### Optional Indexes
- `tasks.due_date`: For due date based queries
- `tasks.priority`: For priority-based sorting

## Data Lifecycle

### Creation
- User accounts created through registration process
- Tasks created by authenticated users
- Creation timestamps automatically set

### Modification
- User updates trigger updated_at timestamp update
- Task completion state changes recorded with timestamps
- All modifications require authentication

### Deletion
- Soft deletion approach preferred for audit trail
- User deletion policy to be determined (cascade vs. orphaned tasks)
- Data retention policies to follow compliance requirements

## API Representation

### User API Model
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "first_name": "Optional",
  "last_name": "Optional",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Task API Model
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "is_completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "due_date": "2023-01-01T00:00:00Z",
  "priority": "medium",
  "user_id": "user-uuid-string"
}
```

## Security Considerations

### Data Protection
- Passwords stored as bcrypt hashes (never plain text)
- Sensitive data encrypted at rest when possible
- JWT tokens validated with secure algorithms
- SQL injection prevention through ORM usage

### Access Control
- Row-level security through user_id filtering
- Authentication required for all data operations
- Authorization checks on every API request
- Audit logging for sensitive operations (future enhancement)