# Implementation Plan: Microservices Event Consumers for Todo System

**Branch**: `006-microservices-event-consumers` | **Date**: 2026-02-02 | **Spec**: [specs/006-microservices-event-consumers/spec.md](specs/006-microservices-event-consumers/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of two event-driven microservices that consume Kafka events produced by the main Todo application. The Notification Service will consume `reminders` topic events and simulate notification delivery, while the Audit Service will consume `task-events` topic events to maintain immutable audit records of all task lifecycle changes.

## Technical Context

**Language/Version**: Python 3.11+ (compatible with existing backend)
**Primary Dependencies**: aiokafka for async Kafka consumption, logging for audit trails, asyncio for async operations
**Storage**: Local file storage for audit records (immutable logs), in-memory for notification service
**Testing**: pytest for unit/integration tests, docker-compose for Kafka testing environment
**Target Platform**: Linux server containers (Docker)
**Project Type**: Multi-service distributed system
**Performance Goals**: Process events with minimal latency, handle concurrent event streams
**Constraints**: No synchronous calls to main backend, no business logic changes, isolated failure tolerance
**Scale/Scope**: Support multiple concurrent consumers per topic, handle typical todo app event volume

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Technology Stack Compliance**: Using Python with external libraries for Kafka integration (allowed as application dependencies for microservices)
- **Architecture Compliance**: Event-driven microservices architecture aligns with specification requirements
- **Integration Compliance**: Services integrate via Kafka only, no direct coupling to main backend
- **Scope Compliance**: Implementation stays within Phase 5 Section C requirements without modifying existing backend

## Project Structure

### Documentation (this feature)

```text
specs/006-microservices-event-consumers/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
apps/
├── notification-service/
│   ├── src/
│   │   ├── consumers/
│   │   │   └── reminder_consumer.py
│   │   ├── models/
│   │   │   └── notification_event.py
│   │   ├── services/
│   │   │   └── notification_service.py
│   │   ├── utils/
│   │   │   └── logger.py
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── config/
│       └── kafka_config.py
├── audit-service/
│   ├── src/
│   │   ├── consumers/
│   │   │   └── task_events_consumer.py
│   │   ├── models/
│   │   │   └── audit_record.py
│   │   ├── services/
│   │   │   └── audit_service.py
│   │   ├── utils/
│   │   │   └── logger.py
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── config/
│       └── kafka_config.py
```

**Structure Decision**: Two separate microservices implemented as independent applications. Each service follows the same structure with consumers, models, services, and configuration. Each service includes structured logging utilities. No shared components to ensure complete isolation - failure of one service must not affect others.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| External Dependencies (Kafka client) | Required for event-driven architecture as specified | Direct database access would violate event-driven pattern requirement |
| File Storage for Audit | Required for immutable audit trail as specified | In-memory storage would lose audit records on restart |
| Multiple Projects | Required by specification for isolation | Single service would violate single-responsibility principle |