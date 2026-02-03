# Quickstart: Microservices Event Consumers for Todo System

## Overview
This guide explains how to set up and run the notification and audit microservices that consume Kafka events from the Todo application.

## Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Access to Kafka cluster (either local or remote)

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Start Kafka infrastructure
```bash
# Navigate to the project root
cd <project-root>

# Start Kafka using docker-compose
docker-compose up -d kafka zookeeper
```

### 3. Set up environment variables
Create a `.env` file in each service directory with the following variables:

For Notification Service (`apps/notification-service/.env`):
```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_CONSUMER_GROUP_ID=notification-service
KAFKA_TOPIC_NAME=reminders
LOG_LEVEL=INFO
```

For Audit Service (`apps/audit-service/.env`):
```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_CONSUMER_GROUP_ID=audit-service
KAFKA_TOPIC_NAME=task-events
AUDIT_LOG_PATH=./audit_logs
LOG_LEVEL=INFO
```

### 4. Install dependencies
```bash
# For notification service
cd apps/notification-service
pip install -r requirements.txt

# For audit service
cd apps/audit-service
pip install -r requirements.txt
```

## Running the Services

### 1. Run Notification Service
```bash
cd apps/notification-service
pip install -r requirements.txt
python src/main.py
```

### 2. Run Audit Service
```bash
cd apps/audit-service
pip install -r requirements.txt
python src/main.py
```

## Docker Deployment

### 1. Build service images
```bash
# From project root
docker build -t notification-service ./apps/notification-service
docker build -t audit-service ./apps/audit-service
```

### 2. Run with Docker
```bash
# Run notification service
docker run -d --env-file ./apps/notification-service/.env notification-service

# Run audit service
docker run -d --env-file ./apps/audit-service/.env audit-service
```

## Testing the Implementation

### 1. Unit Tests
Run the unit tests for both services:

```bash
# For notification service
cd apps/notification-service
python -m pytest test_notification_service.py

# For audit service
cd apps/audit-service
python -m pytest test_audit_service.py
```

### 2. Manual Testing
Verify that both services are consuming events properly by monitoring their logs and confirming that:
- The notification service processes reminder events and logs notification attempts
- The audit service processes task events and creates audit records in the audit log file

## Testing

### 1. Manual Testing
Publish sample events to Kafka topics and observe service behavior:

```bash
# Publish a reminder event to Kafka (using kafka-console-producer)
docker exec -it kafka kafka-console-producer --bootstrap-server localhost:9092 --topic reminders

# Then paste a JSON event like:
{"event_type": "reminder.set", "task_id": "123e4567-e89b-12d3-a456-426614174000", "user_id": "123e4567-e89b-12d3-a456-426614174001", "reminder_time": "2023-12-31T10:00:00Z", "timestamp": "2023-12-30T10:00:00Z", "payload": {"task_title": "Sample Task", "reminder_created_at": "2023-12-30T10:00:00Z"}}
```

### 2. Verify Service Operation
- Check service logs for event processing
- For audit service, verify audit logs are created
- For notification service, verify notification attempts are logged

## Troubleshooting

### Common Issues

1. **Kafka Connection Issues**
   - Verify Kafka is running: `docker ps | grep kafka`
   - Check network connectivity between services and Kafka
   - Verify bootstrap server addresses in configuration

2. **Consumer Group Conflicts**
   - Ensure each service uses a unique consumer group ID
   - Check that consumer group names don't conflict across environments

3. **Topic Does Not Exist**
   - Kafka topics are typically auto-created when accessed
   - Manually create topics if needed: `kafka-topics --create --topic <topic-name> --bootstrap-server <server>`

### Service Logs
- Notification Service: Standard output/error
- Audit Service: Standard output and configured audit log path

## Architecture Notes

- Services are designed to be resilient and continue operating if the main Todo application is unavailable
- Each service operates independently and handles its own failure scenarios
- Events are processed asynchronously without blocking other operations
- Services implement error handling that skips faulty messages and continues processing
- Failure of one service must not affect the operation of the other service
- No retries or dead-letter queues are implemented per requirements