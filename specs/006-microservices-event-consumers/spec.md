# Feature Specification: Microservices Event Consumers for Todo System

**Feature Branch**: `006-microservices-event-consumers`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "sp.specify

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
A clear microservices specification for Phase 5 – Section C."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Notification Delivery (Priority: P1)

As a user who sets reminders on my tasks, I want the system to eventually deliver notifications when the reminder time arrives so that I can be reminded about important tasks without constantly checking the application.

**Why this priority**: This fulfills the core value proposition of the reminder feature by providing timely notifications to users.

**Independent Test**: The notification service can receive reminder events from Kafka and process them independently of the main application, simulating delivery without requiring actual email/SMS integration.

**Acceptance Scenarios**:

1. **Given** a reminder.set event is published to the `reminders` topic, **When** the notification service receives the event, **Then** the service logs the reminder delivery attempt and simulates notification sending
2. **Given** the notification service is running, **When** multiple reminder events are published simultaneously, **Then** each event is processed independently without blocking others

---

### User Story 2 - Audit Trail Visibility (Priority: P1)

As a system administrator or compliance officer, I want to maintain a complete audit trail of all task lifecycle changes so that I can track who did what and when for security and compliance purposes.

**Why this priority**: This provides essential audit capabilities for security, compliance, and debugging purposes.

**Independent Test**: The audit service can receive task lifecycle events from Kafka and store immutable records independently of the main application.

**Acceptance Scenarios**:

1. **Given** a task lifecycle event (created, updated, completed, deleted) is published to the `task-events` topic, **When** the audit service receives the event, **Then** an immutable audit record is stored with complete event details
2. **Given** the audit service is running, **When** multiple task events are published simultaneously, **Then** each event is processed independently and stored as an immutable record

---

### User Story 3 - System Resilience (Priority: P2)

As an operations engineer, I want the main Todo application to continue functioning normally even if the microservices are down or experiencing issues so that user experience is not impacted by auxiliary services.

**Why this priority**: This ensures the core application remains stable and available even when auxiliary services have issues.

**Independent Test**: The main Todo application continues to function normally when the notification and audit services are unavailable.

**Acceptance Scenarios**:

1. **Given** the notification service is down, **When** users create tasks with reminders, **Then** the main application continues to work normally and events are still published to Kafka
2. **Given** the audit service is down, **When** users perform task operations, **Then** the main application continues to work normally and events are still published to Kafka

---

### Edge Cases

- What happens when a microservice fails to process an event?
- How does the system handle event processing delays?
- What occurs when the Kafka connection is temporarily unavailable to a microservice?
- How does the system behave when event processing falls behind the publishing rate?
- What happens if a microservice crashes during event processing?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Notification service MUST consume events from the `reminders` topic when reminder.set events are published
- **FR-002**: Notification service MUST log reminder delivery attempts when processing reminder.set events
- **FR-003**: Notification service MUST simulate notification sending without actual email/SMS integration
- **FR-004**: Audit service MUST consume events from the `task-events` topic for all task lifecycle events
- **FR-005**: Audit service MUST store immutable audit records for task lifecycle events (created, updated, completed, deleted)
- **FR-006**: Both services MUST process events independently without blocking each other
- **FR-007**: Both services MUST handle event processing failures gracefully without affecting other events
- **FR-008**: Main Todo application MUST continue functioning normally even if microservices are down
- **FR-009**: Both services MUST NOT make synchronous calls to the main backend application
- **FR-010**: Both services MUST NOT modify existing business logic in the main application
- **FR-011**: Event consumption MUST be reliable with proper error handling and recovery mechanisms
- **FR-012**: Services MUST continue processing events even if individual events cause errors by logging the error and moving to the next event

### Key Entities *(include if feature involves data)*

- **Notification Event**: Contains reminder information needed for notification delivery simulation
- **Audit Record**: Immutable record of task lifecycle events for compliance and tracking purposes
- **Microservice**: Independent service responsible for processing specific event types

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Notification and audit services run independently without requiring the main application to coordinate with them
- **SC-002**: Events from Kafka are consumed reliably by their respective services with 99%+ success rate when services are operational
- **SC-003**: The main Todo application continues to function normally even when one or both microservices are down
- **SC-004**: Each service processes events independently without blocking or affecting other services
- **SC-005**: Audit records are stored immutably and provide complete visibility into task lifecycle changes
- **SC-006**: Reminder notifications are logged and simulated appropriately when reminder.set events are received