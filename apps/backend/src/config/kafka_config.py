"""Kafka Configuration Module

This module contains all Kafka-related configuration settings for the application.
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class KafkaConfig(BaseSettings):
    """Configuration settings for Kafka integration."""

    # Kafka bootstrap servers
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    # Topic names
    task_events_topic: str = os.getenv("TASK_EVENTS_TOPIC", "task-events")
    reminders_topic: str = os.getenv("REMINDERS_TOPIC", "reminders")
    task_updates_topic: str = os.getenv("TASK_UPDATES_TOPIC", "task-updates")

    # Connection settings
    kafka_max_retries: int = int(os.getenv("KAFKA_MAX_RETRIES", "3"))
    kafka_retry_backoff_ms: int = int(os.getenv("KAFKA_RETRY_BACKOFF_MS", "100"))

    # Security settings (optional)
    kafka_security_protocol: str = os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
    kafka_ssl_cafile: Optional[str] = os.getenv("KAFKA_SSL_CAFILE")
    kafka_ssl_certfile: Optional[str] = os.getenv("KAFKA_SSL_CERTFILE")
    kafka_ssl_keyfile: Optional[str] = os.getenv("KAFKA_SSL_KEYFILE")

    def get_bootstrap_servers_list(self) -> List[str]:
        """Get bootstrap servers as a list of strings."""
        return [server.strip() for server in self.kafka_bootstrap_servers.split(",")]

    @property
    def enabled(self) -> bool:
        """Check if Kafka integration is enabled."""
        return os.getenv("KAFKA_ENABLED", "true").lower() == "true"


# Global instance
kafka_config = KafkaConfig()