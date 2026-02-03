---
id: 7
title: microservices-specification
stage: spec
date_iso: 2026-02-02
surface: agent
model: Claude Sonnet 4.5
feature: 006-microservices-event-consumers
branch: todo-app-phase-5
user: claude
command: sp.specify
labels: ["microservices", "kafka", "event-driven", "specification"]
links:
  spec: "specs/006-microservices-event-consumers/spec.md"
  ticket: null
  adr: null
  pr: null
---

# Microservices Event Consumers Specification

## Files Modified
 - specs/006-microservices-event-consumers/spec.md
 - specs/006-microservices-event-consumers/checklists/requirements.md

## Prompt Text
```
sp.specify

Context:
Phase 5 – Section C introduces microservices that consume Kafka events
produced in Section B.

CRITICAL RULE:
- Existing backend APIs, schemas, and UI must NOT be modified
- Microservices must be event consumers only
- Each service is isolated and single-responsibility

Services to Specify:

1. Notification Service
- Consumes events from the `reminders` topic
- Trigger condition:
  - reminder.set event
- Responsibilities:
  - Log reminder delivery (for now)
  - Simulate notification sending
- No email/SMS integration yet

2. Audit / Activity Log Service
- Consumes events from `task-events`
- Logs full task lifecycle:
  - created
  - updated
  - completed
  - deleted
- Stores immutable audit records

Event Handling Rules:
- Events are processed independently
- Failure in one service does not affect others
- No retry orchestration yet

Constraints:
- No synchronous calls to main backend
- No business logic changes
- No Dapr (comes later)
- No recurrence

Acceptance Criteria:
- Services run independently
- Events are consumed reliably
- Main app continues working if services are down

Output:
A clear microservices specification for Phase 5 – Section C.
```

## Response Text
Created comprehensive specification for microservices event consumers, including:
- Two independent services: Notification and Audit
- User scenarios with acceptance criteria
- Functional requirements covering both services
- Success criteria for measuring outcomes
- Edge cases for error handling
- Quality checklist to validate the specification

The specification covers all requirements from the user input, with clear separation between the notification service (handling reminder events) and audit service (maintaining immutable logs of task lifecycle events). Both services operate independently without modifying the existing backend.

## Outcome
Successfully created a complete specification for the microservices event consumers feature that meets all requirements and is ready for planning.

## Evaluation
The specification addresses all user requirements with clear user stories, functional requirements, and success criteria. It maintains proper separation of concerns between services and adheres to the constraint of not modifying existing backend systems.