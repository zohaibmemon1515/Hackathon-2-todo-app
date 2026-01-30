# Implementation Plan: Advanced Todo Features - Phase 5

**Feature**: 005-advanced-todo-features
**Created**: 2026-01-30
**Status**: Draft
**Author**: Claude

## Technical Context

This plan outlines the incremental enhancement of the existing Todo application with advanced features including tags, search, advanced filtering, sorting, recurrence, and reminder configuration. The system currently supports basic CRUD operations, priority levels, and due dates.

**Current Tech Stack:**
- Backend: Python 3.11+, FastAPI, SQLModel, PostgreSQL (Neon)
- Frontend: TypeScript, Next.js 16+, React
- Database: Neon Serverless PostgreSQL

**Key Components to Extend:**
- Task model (apps/backend/src/models/task.py)
- Task API endpoints (apps/backend/src/api/tasks.py)
- Task service (apps/backend/src/services/task_service.py)
- Frontend task components (apps/frontend/src/components/tasks/)

**Unknowns:**
- Database migration strategy for adding new fields [NEEDS CLARIFICATION]
- Tag storage approach (separate table vs JSON field) [NEEDS CLARIFICATION]
- Specific reminder configuration format [NEEDS CLARIFICATION]

## Constitution Check

**Compliance Status**: Compliant with current system architecture principles

**Analysis**: This plan extends the existing multi-tier architecture (model/service/interface) without violating separation of concerns. All changes maintain backward compatibility as required.

**Potential Issues**:
- Need to ensure no breaking changes to existing API contracts
- Must maintain performance standards with new query operations

## Gates

### Gate 1: Architecture Alignment
✅ **PASS**: Plan follows existing architecture patterns and extends current components

### Gate 2: Backwards Compatibility
✅ **PASS**: All new features are optional parameters/features that won't break existing clients

### Gate 3: Performance Impact
⚠️ **REVIEW**: New search/filter operations require indexing strategy review

### Gate 4: Security Impact
✅ **PASS**: All operations remain user-scoped with existing authentication/authorization

## Phase 0: Research & Resolution

### research.md

#### Decision: Tag Storage Strategy
**Rationale**: Implement tags as a separate "task_tags" table with many-to-many relationship to maintain data normalization and efficient querying. This allows for indexed lookups and follows SQL best practices.
**Alternatives considered**: JSON field in task table (simpler but less efficient for filtering), separate tags table with linking (most normalized but complex joins)

#### Decision: Search Implementation
**Rationale**: Use PostgreSQL's built-in full-text search capabilities with indexes on title and description fields for optimal performance. This provides efficient fuzzy matching while maintaining good response times.
**Alternatives considered**: LIKE queries (slower for large datasets), external search engine (overkill for this scale)

#### Decision: Recurrence and Reminder Storage
**Rationale**: Store as JSON fields in the existing task table since these are optional, structured data that don't require frequent querying. This minimizes schema changes while maintaining flexibility.
**Alternatives considered**: Separate tables (more normalized but adds complexity), separate service (violates monolithic approach)

## Phase 1: Design & Contracts

### data-model.md

#### Extended Task Model
```
Task (extends existing model):
- id: int (primary key, auto-increment)
- title: string (required, 1-255 chars)
- description: string (optional, max 1000 chars)
- is_completed: bool (default: false)
- due_date: datetime (optional)
- priority: enum (low, medium, high; default: medium)
- tags: List<string> (optional, stored as separate table relationship)
- recurrence_rule: JSON (optional, structure: {frequency: daily|weekly|monthly, interval: int, end_condition: {type: on_date|after_occurrences, value: date|count}})
- reminder_config: JSON (optional, structure: {offset_minutes: int, notification_method: email|push})
- user_id: UUID (foreign key to user)
- created_at: datetime (auto-set)
- updated_at: datetime (auto-set)
```

#### Tag Model
```
Tag:
- id: int (primary key)
- name: string (required, user-scoped)
- user_id: UUID (foreign key to user)
- created_at: datetime (auto-set)

TaskTag (junction table):
- task_id: int (foreign key to task)
- tag_id: int (foreign key to tag)
```

#### SearchParams Model
```
SearchParams:
- query: string (search keywords)
- tags: List<string> (filter by tags)
- due_date_from: datetime (filter due date range start)
- due_date_to: datetime (filter due date range end)
- sort_by: enum (title, priority, due_date, created_at)
- sort_order: enum (asc, desc)
- completed: bool (existing filter, optional)
- limit: int (pagination)
- offset: int (pagination)
```

### API Contracts

#### Extended GET /tasks endpoint
```
GET /tasks?query={keywords}&tags[]={tag1}&tags[]={tag2}&due_date_from={date}&due_date_to={date}&sort_by={field}&sort_order={asc|desc}&completed={true|false}&limit={int}&offset={int}

Response: {
  "tasks": [TaskRead...],
  "total": int,
  "limit": int,
  "offset": int
}
```

#### Updated POST /tasks endpoint
Request body now includes:
```
{
  "title": string,
  "description": string (optional),
  "due_date": datetime (optional),
  "priority": enum (optional),
  "tags": string[] (optional),
  "recurrence_rule": object (optional),
  "reminder_config": object (optional)
}
```

#### Updated PUT/PATCH /tasks/{id} endpoints
Support the same extended fields as CREATE

### quickstart.md

#### Setup for Advanced Features
1. Run database migrations to add tags table and extend task model
2. Update environment variables if needed for search indexing
3. Deploy backend with extended API endpoints
4. Update frontend to support new fields and filtering options

## Phase 2: Implementation Approach

### Backend Implementation
1. Extend Task model with new fields and relationships
2. Update TaskCreate, TaskUpdate, TaskPatch schemas
3. Enhance task service with search and filtering logic
4. Update API endpoints to accept new parameters
5. Add database migrations for schema changes

### Frontend Implementation
1. Extend Task form components with new fields
2. Update Task list to support search and advanced filtering
3. Add sorting controls to task list view
4. Implement tag selection UI components

### Database Changes
1. Create tags and task_tags tables
2. Add indexes for efficient searching and filtering
3. Maintain existing indexes for backward compatibility

## Risk Analysis

### High-Risk Areas
- Performance degradation with complex search queries
- Database migration safety in production

### Mitigation Strategies
- Implement proper indexing strategy before rollout
- Test migration on backup copy first
- Add performance monitoring for new query patterns

## Dependencies

- SQLModel ORM capabilities for relationships
- PostgreSQL full-text search features
- Existing authentication and authorization middleware