# Notification Service

This service consumes reminder events from the `reminders` Kafka topic and simulates notification delivery.

## Purpose

The notification service listens to reminder events and logs delivery attempts. It serves as a placeholder for future notification functionality (email, SMS, push notifications).

## Configuration

The service can be configured using environment variables:

- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker addresses (default: `localhost:9092`)
- `KAFKA_CONSUMER_GROUP_ID`: Consumer group ID (default: `notification-service`)
- `KAFKA_TOPIC_NAME`: Topic to consume from (default: `reminders`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## Running the Service

### With Python

```bash
cd apps/notification-service
pip install -r requirements.txt
python -m src.main
```

### With Docker

```bash
cd apps/notification-service
docker build -t notification-service .
docker run -e KAFKA_BOOTSTRAP_SERVERS=kafka:9092 notification-service
```

## Features

- Consumes `reminder.set` events from the `reminders` topic
- Simulates notification delivery
- Logs delivery attempts
- Handles malformed events gracefully
- Graceful shutdown handling