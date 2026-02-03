# Audit Service

This service consumes task events from the `task-events` Kafka topic and maintains immutable audit records.

## Purpose

The audit service listens to task lifecycle events (create, update, complete, delete) and stores them as immutable audit records for compliance and tracking purposes.

## Configuration

The service can be configured using environment variables:

- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker addresses (default: `localhost:9092`)
- `KAFKA_CONSUMER_GROUP_ID`: Consumer group ID (default: `audit-service`)
- `KAFKA_TOPIC_NAME`: Topic to consume from (default: `task-events`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `AUDIT_LOG_PATH`: Path for audit log storage (default: `./audit_logs/audit.log`)

## Running the Service

### With Python

```bash
cd apps/audit-service
pip install -r requirements.txt
python -m src.main
```

### With Docker

```bash
cd apps/audit-service
docker build -t audit-service .
docker run -e KAFKA_BOOTSTRAP_SERVERS=kafka:9092 -e AUDIT_LOG_PATH=/app/audit_logs/audit.log audit-service
```

## Features

- Consumes task lifecycle events from the `task-events` topic
- Creates immutable audit records for each event
- Stores audit records in file-based append-only storage
- Handles malformed events gracefully
- Graceful shutdown handling