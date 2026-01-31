# Quickstart: Kafka Event Integration

## Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Poetry or pip for dependency management

## Local Development Setup

### 1. Start Kafka Environment
```bash
# Using Docker Compose
docker-compose up -d kafka zookeeper

# Or using a Kafka container directly
docker run -d --name kafka-local \
  -p 9092:9092 \
  -e KAFKA_BROKER_ID=1 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  confluentinc/cp-kafka:latest
```

### 2. Create Kafka Topics
```bash
# Create required topics
kafka-topics --create --topic task-events --bootstrap-server localhost:9092
kafka-topics --create --topic reminders --bootstrap-server localhost:9092
kafka-topics --create --topic task-updates --bootstrap-server localhost:9092
```

### 3. Install Dependencies
```bash
# Add aiokafka to your project
poetry add aiokafka
# or
pip install aiokafka
```

### 4. Configure Kafka Settings
```python
# Example configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TASK_EVENTS_TOPIC = 'task-events'
KAFKA_REMINDERS_TOPIC = 'reminders'
KAFKA_TASK_UPDATES_TOPIC = 'task-updates'
```

## Running the Application
1. Start your Kafka cluster
2. Run your application normally
3. Events will be published automatically when task operations occur
4. Monitor events using Kafka consumer tools

## Testing Event Publishing
```bash
# Consume events from task-events topic
kafka-console-consumer --topic task-events --from-beginning --bootstrap-server localhost:9092
```