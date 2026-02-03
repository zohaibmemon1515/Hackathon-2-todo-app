---
id: 9
title: microservices-tasks-generation
stage: tasks
date_iso: 2026-02-02
surface: agent
model: Claude Sonnet 4.5
feature: 006-microservices-event-consumers
branch: todo-app-phase-5
user: claude
command: sp.tasks
labels: ["microservices", "kafka", "event-driven", "tasks", "implementation"]
links:
  spec: "specs/006-microservices-event-consumers/spec.md"
  plan: "specs/006-microservices-event-consumers/plan.md"
  tasks: "specs/006-microservices-event-consumers/tasks.md"
  ticket: null
  adr: null
  pr: null
---

# Microservices Event Consumers Tasks Generation

## Files Modified
 - specs/006-microservices-event-consumers/tasks.md

## Prompt Text
```
sp.tasks

Context:
Generate implementation tasks for Phase 5 – Section C.

Task Rules:
- Tasks must ADD microservices only
- Tasks must NOT modify existing backend
- Tasks must be ordered and testable

Task Groups:

1. Shared Tasks
- Define common Kafka consumer configuration
- Define event deserialization helpers

2. Notification Service Tasks
- Create notification service project/module
- Implement consumer for `reminders`
- Log reminder execution
- Handle malformed events safely

3. Audit Service Tasks
- Create audit service project/module
- Implement consumer for `task-events`
- Store audit logs (DB or file)
- Ensure immutability

4. Reliability Tasks
- Graceful shutdown handling
- Safe logging
- Consumer offset management

Each Task Must Include:
- Task ID
- Service name
- Trigger topic
- Expected behavior
- Files/modules affected
- Spec reference

Output:
An ordered task list for Section C microservices.
```

## Response Text
Generated comprehensive implementation tasks for microservices event consumers, organized into 6 phases:
- Phase 1: Setup (project initialization)
- Phase 2: Foundational (shared infrastructure)
- Phase 3: User Story 1 - Notification Delivery (P1 priority)
- Phase 4: User Story 2 - Audit Trail Visibility (P1 priority)
- Phase 5: Reliability & Error Handling
- Phase 6: Polish & Cross-Cutting Concerns

Tasks include creating directory structures, implementing consumers, services, models, configuration, error handling, and testing. Each task follows the required checklist format with sequential IDs (T001-T039), appropriate story labels [US1], [US2], and file paths. Parallel execution opportunities identified between services.

## Outcome
Successfully created an ordered task list for the microservices event consumers feature that follows the required format and enables independent implementation and testing of user stories.

## Evaluation
The generated tasks fulfill all requirements:
- Tasks ADD microservices only (no existing backend modification)
- Tasks are ordered and testable
- Each task includes ID, service name, trigger topic, expected behavior, files affected, and spec reference
- Tasks organized by user story for independent implementation
- Parallel execution opportunities identified
- All tasks follow the required checklist format