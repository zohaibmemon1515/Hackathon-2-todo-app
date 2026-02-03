# Implementation Tasks: Microservices Event Consumers for Todo System

**Feature**: Microservices Event Consumers for Todo System
**Created**: 2026-02-02
**Status**: Ready for Implementation
**Spec Reference**: [specs/006-microservices-event-consumers/spec.md](spec.md)

## Dependencies

- User Story 1 (Notification Delivery) and User Story 2 (Audit Trail Visibility) can be developed in parallel
- User Story 3 (System Resilience) is inherent in the architecture and implemented across all other tasks

## Parallel Execution Opportunities

- Notification Service and Audit Service can be developed independently
- Each service's components (models, consumers, services, config) can be developed in parallel within each service

---

## Phase 1: Setup

### Goal
Initialize project structure and shared configuration for both microservices.

### Tasks

- [x] T001 Create notification-service directory structure at apps/notification-service/
- [x] T002 Create audit-service directory structure at apps/audit-service/
- [x] T003 [P] Create shared requirements.txt files for both services
- [x] T004 [P] Initialize Dockerfile for notification-service
- [x] T005 [P] Initialize Dockerfile for audit-service
- [x] T006 Create source directory structure for notification-service
- [x] T007 Create source directory structure for audit-service

---

## Phase 2: Foundational

### Goal
Establish common infrastructure and utilities that both services will use.

### Tasks

- [x] T008 Define common Kafka consumer configuration models
- [x] T009 [P] Create event deserialization helper functions for both services
- [x] T010 Implement structured logging utilities for both services
- [x] T011 Set up consumer configuration models for both services

---

## Phase 3: User Story 1 - Notification Delivery (Priority: P1)

### Goal
Implement notification service that consumes reminder events and logs delivery attempts.

### Independent Test Criteria
The notification service can receive reminder events from Kafka and process them independently of the main application, simulating delivery without requiring actual email/SMS integration.

### Acceptance Scenarios
1. Given a reminder.set event is published to the `reminders` topic, When the notification service receives the event, Then the service logs the reminder delivery attempt and simulates notification sending
2. Given the notification service is running, When multiple reminder events are published simultaneously, Then each event is processed independently without blocking others

### Tasks

- [x] T012 [US1] Create NotificationEvent model in apps/notification-service/src/models/notification_event.py
- [x] T013 [US1] Create NotificationLogEntry model in apps/notification-service/src/models/notification_event.py
- [x] T014 [US1] Implement reminder consumer in apps/notification-service/src/consumers/reminder_consumer.py
- [x] T015 [US1] Implement notification service logic in apps/notification-service/src/services/notification_service.py
- [x] T016 [US1] Configure Kafka settings for notification service in apps/notification-service/config/kafka_config.py
- [x] T017 [US1] Create main application entry point for notification service in apps/notification-service/src/main.py
- [x] T018 [US1] Implement error handling for malformed events in reminder consumer

---

## Phase 4: User Story 2 - Audit Trail Visibility (Priority: P1)

### Goal
Implement audit service that consumes task events and stores immutable audit records.

### Independent Test Criteria
The audit service can receive task lifecycle events from Kafka and store immutable records independently of the main application.

### Acceptance Scenarios
1. Given a task lifecycle event (created, updated, completed, deleted) is published to the `task-events` topic, When the audit service receives the event, Then an immutable audit record is stored with complete event details
2. Given the audit service is running, When multiple task events are published simultaneously, Then each event is processed independently and stored as an immutable record

### Tasks

- [x] T019 [US2] Create AuditRecord model in apps/audit-service/src/models/audit_record.py
- [x] T020 [US2] Create TaskEvent model in apps/audit-service/src/models/audit_record.py
- [x] T021 [US2] Implement task events consumer in apps/audit-service/src/consumers/task_events_consumer.py
- [x] T022 [US2] Implement audit service logic in apps/audit-service/src/services/audit_service.py
- [x] T023 [US2] Configure Kafka settings for audit service in apps/audit-service/config/kafka_config.py
- [x] T024 [US2] Create main application entry point for audit service in apps/audit-service/src/main.py
- [x] T025 [US2] Implement file-based audit log storage in audit service
- [x] T026 [US2] Implement error handling for malformed events in task events consumer

---

## Phase 5: Reliability & Error Handling

### Goal
Implement robust error handling, graceful shutdown, and consumer offset management.

### Tasks

- [x] T027 Implement graceful shutdown handling for notification service
- [x] T028 Implement graceful shutdown handling for audit service
- [x] T029 [P] Enhance error logging for both services
- [x] T030 [P] Implement safe consumer offset management for both services
- [x] T031 Add health check endpoints for both services
- [x] T032 Implement retry logic for Kafka connection in both services

---

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with testing, documentation, and deployment configuration.

### Tasks

- [x] T033 Write unit tests for notification service components
- [x] T034 Write unit tests for audit service components
- [x] T035 Create comprehensive README for both services
- [ ] T036 Set up CI/CD pipeline for both services
- [ ] T037 Document deployment procedures for both services
- [ ] T038 Perform integration testing between services and Kafka
- [x] T039 Update quickstart guide with complete deployment instructions

---

## Implementation Strategy

### MVP Scope
The MVP includes User Story 1 and User Story 2, which can be developed in parallel:
- Basic notification service that consumes reminder events and logs them
- Basic audit service that consumes task events and stores audit logs

### Incremental Delivery
1. **Iteration 1**: Complete Phase 1 (Setup) and Phase 2 (Foundational)
2. **Iteration 2**: Complete User Story 1 (Notification Service)
3. **Iteration 3**: Complete User Story 2 (Audit Service)
4. **Iteration 4**: Complete Phase 5 (Reliability) and Phase 6 (Polish)

### Task Dependencies
- T012-T018 depend on Phase 1 and Phase 2 completion
- T019-T026 depend on Phase 1 and Phase 2 completion
- All later phases depend on earlier phases