import os
from src.models.consumer_config import ConsumerConfig

def get_audit_consumer_config() -> ConsumerConfig:
    """Get Kafka configuration for audit service."""
    return ConsumerConfig(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        group_id=os.getenv("KAFKA_CONSUMER_GROUP_ID", "audit-service"),
        topic_name=os.getenv("KAFKA_TOPIC_NAME", "task-events"),
        auto_offset_reset=os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest"),
        enable_auto_commit=os.getenv("KAFKA_ENABLE_AUTO_COMMIT", "true").lower() == "true",
        max_poll_records=int(os.getenv("KAFKA_MAX_POLL_RECORDS", "10")),
        session_timeout_ms=int(os.getenv("KAFKA_SESSION_TIMEOUT_MS", "30000")),
        graceful_shutdown_timeout=int(os.getenv("GRACEFUL_SHUTDOWN_TIMEOUT", "30"))
    )