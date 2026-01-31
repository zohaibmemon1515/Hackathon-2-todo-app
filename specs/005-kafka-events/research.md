# Research: Kafka Event-Driven Layer for Todo System

## Decision: Kafka Integration Approach
**Rationale**: Based on the feature requirements, we need to integrate Apache Kafka as an event streaming platform to enable event-driven architecture for the Todo system. This allows decoupling of services and enables future extensibility for notifications, analytics, and real-time updates.

**Alternatives considered**:
- RabbitMQ: More complex setup, better for direct messaging patterns
- Redis Pub/Sub: Simpler but lacks durability and replay capabilities
- AWS SQS/SNS: Cloud-native but adds external dependencies
- Apache Pulsar: Similar capabilities but more complex than Kafka for this use case

## Decision: Kafka Client Library
**Rationale**: For Python applications, aiokafka is the preferred choice as it provides asyncio support for non-blocking event publishing, which aligns with the requirement for async, non-blocking publishing.

**Alternatives considered**:
- confluent-kafka: Lower-level, synchronous by default
- kafka-python: Synchronous, older library with less active maintenance

## Decision: Event Publishing Strategy
**Rationale**: Events must be published AFTER successful database commits to ensure data consistency. Using a fire-and-forget approach with error handling ensures that Kafka failures do not break the core API functionality, meeting the requirement that "Task CRUD works even if Kafka is unavailable".

**Alternatives considered**:
- Transactional publishing: More complex, could block API responses
- Retry mechanisms: Adds complexity, could delay API responses
- Batch publishing: Doesn't meet real-time requirements for UI synchronization

## Decision: Topic Design
**Rationale**: Three separate topics allow for different consumers to handle different types of events appropriately:
- task-events: For audit trails, analytics, and downstream services
- reminders: For dedicated reminder/notification services
- task-updates: For real-time UI synchronization

**Alternatives considered**:
- Single topic with message routing: Less granular control over consumer groups
- Topic per event type: Would create too many topics, harder to manage

## Decision: Local Development Setup
**Rationale**: Using Docker Compose with Kafka and Zookeeper provides an easy way to set up a local development environment that matches production-like conditions.

**Alternatives considered**:
- Redpanda: Kafka-compatible but lighter weight
- Confluent Cloud: Production-ready but adds external dependencies for development