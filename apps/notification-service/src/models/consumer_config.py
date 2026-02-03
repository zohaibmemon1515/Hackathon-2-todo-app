from typing import Optional
from pydantic import BaseModel


class ConsumerConfig(BaseModel):
    """Configuration for Kafka consumer"""
    bootstrap_servers: str = "localhost:9092"
    group_id: str
    topic_name: str
    auto_offset_reset: str = "earliest"
    enable_auto_commit: bool = True
    max_poll_records: int = 10
    session_timeout_ms: int = 30000
    graceful_shutdown_timeout: int = 30