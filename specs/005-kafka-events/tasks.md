# Tasks: Kafka Event-Driven Layer for Todo System

**Feature**: 005-kafka-events | **Date**: 2026-02-01 | **Plan**: specs/005-kafka-events/plan.md

## Overview

Incremental implementation of Kafka-based event publishing for task lifecycle changes. All existing CRUD logic remains unchanged; only event publishing is added.

## Task Groups

### Group 1: Infrastructure Setup
**Objective**: Set up Kafka infrastructure for development and production

#### Task 1.1: Add Kafka Configuration [X]
- **ID**: T1.1
- **Description**: Add Kafka configuration settings to the application
- **Trigger**: Application startup
- **Dependencies**: None
- **Files**: `apps/backend/src/config/kafka_config.py`
- **Spec Reference**: FR-010 (Kafka transport mechanism)
- **Acceptance Criteria**:
  - Configuration includes bootstrap servers, topic names
  - Settings can be overridden via environment variables

#### Task 1.2: Add Kafka Dependencies [X]
- **ID**: T1.2
- **Description**: Add aiokafka as project dependency
- **Trigger**: Development environment setup
- **Dependencies**: None
- **Files**: `apps/backend/pyproject.toml`, `apps/backend/requirements.txt`
- **Spec Reference**: FR-010 (Kafka transport mechanism)
- **Acceptance Criteria**:
  - aiokafka added to dependencies
  - Dependency versions compatible with existing stack

#### Task 1.3: Create Docker Compose for Kafka [X]
- **ID**: T1.3
- **Description**: Set up local Kafka and Zookeeper containers
- **Trigger**: Local development environment setup
- **Dependencies**: None
- **Files**: `docker-compose.kafka.yml`
- **Spec Reference**: FR-010 (Kafka transport mechanism)
- **Acceptance Criteria**:
  - Kafka and Zookeeper containers defined
  - Topics created automatically on startup

### Group 2: Event Publisher Implementation
**Objective**: Implement event publishers that publish after successful DB commits

#### Task 2.1: Create Kafka Service [X]
- **ID**: T2.1
- **Description**: Create a service class for Kafka operations
- **Trigger**: Event publishing required
- **Dependencies**: T1.1, T1.2
- **Files**: `apps/backend/src/services/kafka_service.py`
- **Spec Reference**: FR-001 (publish events to Kafka topics)
- **Acceptance Criteria**:
  - Service can connect to Kafka broker
  - Provides async methods for publishing events
  - Implements graceful error handling

#### Task 2.2: Define Event Schemas [X]
- **ID**: T2.2
- **Description**: Create data classes for event schemas
- **Trigger**: Event publishing required
- **Dependencies**: None
- **Files**: `apps/backend/src/schemas/event_schemas.py`
- **Spec Reference**: FR-002, FR-003, FR-005 (event payloads)
- **Acceptance Criteria**:
  - TaskEvent schema with all required fields
  - ReminderEvent schema with required fields
  - Proper serialization methods

#### Task 2.3: Publish task.created Events [X]
- **ID**: T2.3
- **Description**: Publish task.created events after successful task creation
- **Trigger**: Successful task creation in DB
- **Dependencies**: T2.1, T2.2
- **Files**: `apps/backend/src/services/task_service.py`
- **Spec Reference**: FR-002 (task.created event), FR-008 (after DB commit)
- **Acceptance Criteria**:
  - Event published to `task-events` topic after DB commit
  - Event contains all required fields
  - Original API behavior unchanged

#### Task 2.4: Publish task.updated Events [X]
- **ID**: T2.4
- **Description**: Publish task.updated events after successful task updates
- **Trigger**: Successful task update in DB
- **Dependencies**: T2.1, T2.2
- **Files**: `apps/backend/src/services/task_service.py`
- **Spec Reference**: FR-002 (task.updated event), FR-008 (after DB commit)
- **Acceptance Criteria**:
  - Event published to `task-events` topic after DB commit
  - Event contains all required fields
  - Original API behavior unchanged

#### Task 2.5: Publish task.completed Events [X]
- **ID**: T2.5
- **Description**: Publish task.completed events after successful task completion
- **Trigger**: Successful task completion in DB
- **Dependencies**: T2.1, T2.2
- **Files**: `apps/backend/src/services/task_service.py`
- **Spec Reference**: FR-002 (task.completed event), FR-008 (after DB commit)
- **Acceptance Criteria**:
  - Event published to `task-events` topic after DB commit
  - Event contains all required fields
  - Original API behavior unchanged

#### Task 2.6: Publish task.deleted Events [X]
- **ID**: T2.6
- **Description**: Publish task.deleted events after successful task deletion
- **Trigger**: Successful task deletion in DB
- **Dependencies**: T2.1, T2.2
- **Files**: `apps/backend/src/services/task_service.py`
- **Spec Reference**: FR-002 (task.deleted event), FR-008 (after DB commit)
- **Acceptance Criteria**:
  - Event published to `task-events` topic after DB commit
  - Event contains all required fields
  - Original API behavior unchanged

#### Task 2.7: Publish reminder events [X]
- **ID**: T2.7
- **Description**: Publish reminder events when tasks have reminder_at configured
- **Trigger**: Task with reminder_at is created or updated
- **Dependencies**: T2.1, T2.2
- **Files**: `apps/backend/src/services/task_service.py`
- **Spec Reference**: FR-004 (reminder events), FR-008 (after DB commit)
- **Acceptance Criteria**:
  - Event published to `reminders` topic after DB commit
  - Event contains required reminder fields
  - Only published when reminder_at is set

### Group 3: Consumer Implementation
**Objective**: Implement basic consumers for event monitoring

#### Task 3.1: Create Basic Task Events Consumer [X]
- **ID**: T3.1
- **Description**: Create a basic consumer for task-events topic that logs events
- **Trigger**: Event received on task-events topic
- **Dependencies**: T1.1, T1.2
- **Files**: `apps/backend/src/services/task_events_consumer.py`
- **Spec Reference**: FR-002 (task event consumption)
- **Acceptance Criteria**:
  - Consumer connects to task-events topic
  - Logs received events with structured format
  - Runs as a background service

#### Task 3.2: Create Basic Reminders Consumer [X]
- **ID**: T3.2
- **Description**: Create a basic consumer for reminders topic that logs events
- **Trigger**: Event received on reminders topic
- **Dependencies**: T1.1, T1.2
- **Files**: `apps/backend/src/services/reminders_consumer.py`
- **Spec Reference**: FR-004 (reminder event consumption)
- **Acceptance Criteria**:
  - Consumer connects to reminders topic
  - Logs received events with structured format
  - Runs as a background service

### Group 4: Safety and Error Handling
**Objective**: Ensure robust error handling and graceful degradation

#### Task 4.1: Implement Kafka Error Handling [X]
- **ID**: T4.1
- **Description**: Implement error handling for Kafka operations
- **Trigger**: Kafka connection/publishing failure
- **Dependencies**: T2.1
- **Files**: `apps/backend/src/services/kafka_service.py`
- **Spec Reference**: FR-007 (independent of Kafka availability)
- **Acceptance Criteria**:
  - Errors are logged appropriately
  - Failures don't break core API functionality
  - Graceful degradation when Kafka is unavailable

#### Task 4.2: Add Structured Logging [X]
- **ID**: T4.2
- **Description**: Add structured logging for event operations
- **Trigger**: Event publishing or consumption
- **Dependencies**: T2.1, T3.1, T3.2
- **Files**: `apps/backend/src/utils/logging.py`
- **Spec Reference**: FR-007 (logging and monitoring)
- **Acceptance Criteria**:
  - Events are logged with structured format
  - Error conditions are properly logged
  - Performance metrics are captured

#### Task 4.3: Test Resilience to Kafka Downtime [X]
- **ID**: T4.3
- **Description**: Verify that core functionality works when Kafka is unavailable
- **Trigger**: Manual testing and integration tests
- **Dependencies**: All previous tasks
- **Files**: `apps/backend/tests/integration/test_kafka_resilience.py`
- **Spec Reference**: FR-007 (independent of Kafka availability)
- **Acceptance Criteria**:
  - Task CRUD operations work when Kafka is down
  - No exceptions thrown during Kafka outages
  - Proper logging of connectivity issues

## Task Dependencies

- T1.1, T1.2 → T2.1
- T2.1 → T2.2, T2.3, T2.4, T2.5, T2.6, T2.7
- T2.2 → T2.3, T2.4, T2.5, T2.6, T2.7
- T1.1, T1.2 → T3.1, T3.2
- T2.1 → T4.1
- T4.1, T3.1, T3.2 → T4.2
- All tasks → T4.3

## Success Metrics

- Task CRUD operations continue to work when Kafka is unavailable
- Events are published consistently after successful database commits
- Existing API responses remain unchanged
- Error conditions are properly logged
- Performance impact is minimal (<5% response time increase)