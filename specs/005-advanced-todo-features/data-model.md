# Data Model: Advanced Todo Features

## Extended Task Model

### Task Entity (apps/backend/src/models/task.py)
```
Task (extends existing model):
- id: int (primary key, auto-increment)
- title: string (required, 1-255 chars)
- description: string (optional, max 1000 chars)
- is_completed: bool (default: false)
- due_date: datetime (optional, timestamp with timezone)
- priority: enum (low, medium, high; default: medium)
- recurrence_rule: JSONB (optional, structure: {frequency: "daily|weekly|monthly", interval: int, end_condition: {type: "on_date|after_occurrences", value: date|count}})
- reminder_config: JSONB (optional, structure: {offset_minutes: int, notification_method: "email|push"})
- user_id: uuid.UUID (foreign key to user, indexed)
- created_at: datetime (auto-set, indexed)
- updated_at: datetime (auto-set, indexed)
```

### Tag Entity
```
Tag:
- id: int (primary key, auto-increment)
- name: string (required, 1-50 chars, user-scoped)
- user_id: uuid.UUID (foreign key to user, indexed)
- created_at: datetime (auto-set, indexed)
- UNIQUE constraint: (name, user_id)
```

### Task-Tag Junction Table
```
TaskTag (many-to-many relationship):
- task_id: int (foreign key to task, indexed)
- tag_id: int (foreign key to tag, indexed)
- created_at: datetime (auto-set)
- PRIMARY KEY: (task_id, tag_id)
- FOREIGN KEY: task_id references Task(id) ON DELETE CASCADE
- FOREIGN KEY: tag_id references Tag(id) ON DELETE CASCADE
```

## Search and Filtering Parameters

### SearchParams Model
```
SearchParams:
- query: string (optional, search keywords for title/description)
- tags: List<string> (optional, filter by tag names)
- due_date_from: datetime (optional, filter due date range start)
- due_date_to: datetime (optional, filter due date range end)
- sort_by: enum ("title", "priority", "due_date", "created_at", "updated_at") (optional, default: "created_at")
- sort_order: enum ("asc", "desc") (optional, default: "desc")
- completed: bool (optional, existing filter)
- limit: int (optional, pagination, default: 50, max: 100)
- offset: int (optional, pagination, default: 0)
```

## Relationship Diagram

```
[User] 1 ---- * [Task]
[User] 1 ---- * [Tag]
[Task] * ---- * [Tag] (via TaskTag junction)
```

## Indexing Strategy

### Required Indexes
1. **Task table**:
   - Primary: id (auto-indexed)
   - Composite: (user_id, is_completed) - for user-task filtering
   - Individual: due_date - for date range queries
   - Individual: created_at - for sorting
   - Full-text: GIN index on (to_tsvector('english', title || ' ' || coalesce(description, ''))) - for search

2. **Tag table**:
   - Primary: id (auto-indexed)
   - Composite: (user_id, name) - for user-tag uniqueness and lookup
   - Individual: user_id - for user-specific tag queries

3. **TaskTag table**:
   - Primary: (task_id, tag_id) (auto-indexed)
   - Individual: task_id - for task-tag lookups
   - Individual: tag_id - for tag-based filtering