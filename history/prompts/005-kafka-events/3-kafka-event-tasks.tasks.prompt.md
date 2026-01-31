---
id: 3
title: "Kafka Event Tasks"
stage: tasks
date_iso: 2026-02-01
surface: agent
model: Claude Sonnet 4.5
feature: kafka-events
branch: 005-kafka-events
user: user
command: sp.tasks
labels: ["kafka", "events", "todo", "tasks"]
links:
  spec: "specs/005-kafka-events/spec.md"
  plan: "specs/005-kafka-events/plan.md"
  tasks: "specs/005-kafka-events/tasks.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/005-kafka-events/tasks.md"
  - "history/prompts/005-kafka-events/3-kafka-event-tasks.tasks.prompt.md"
tests_yaml: []
prompt_text: |
  sp.tasks

  Context:
  Generate incremental tasks for Phase 5 – Section B.

  Task Rules:
  - ADD event publishing only
  - DO NOT change existing CRUD logic
  - Exclude recurrence entirely

  Task Groups:

  1. Infrastructure
  - Setup Kafka/Redpanda
  - Create required topics

  2. Producers
  - Publish task.created event
  - Publish task.updated event
  - Publish task.completed event
  - Publish task.deleted event
  - Publish reminders event when reminder_at exists

  3. Consumers
  - Basic consumer for task-events (logging only)
  - Basic consumer for reminders (logging only)

  4. Safety
  - Graceful handling of Kafka downtime
  - Structured logging

  Each Task Includes:
  - Task ID
  - Trigger condition
  - Event schema
  - Files affected
  - Spec reference

  Output:
  An ordered task list for Section B (no recurrence).
response_text: |
  Successfully created a comprehensive task list for Kafka event-driven layer implementation including:
  - Infrastructure setup tasks (configuration, dependencies, Docker compose)
  - Event publisher implementation tasks (service, schemas, individual event types)
  - Consumer implementation tasks (basic consumers for both topics)
  - Safety and error handling tasks (resilience, logging, testing)
  - All tasks properly organized with dependencies and acceptance criteria
outcome: Complete task breakdown created with proper ordering and dependencies
evaluation: Tasks are ready for implementation phase
---
