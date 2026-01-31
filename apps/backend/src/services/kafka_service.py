"""Kafka Service Module

This module provides a service for publishing events to Kafka topics.
It implements fire-and-forget publishing with proper error handling
to ensure that Kafka failures don't break core API functionality.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from aiokafka import AIOKafkaProducer
from dateutil.parser import isoparse

from ..config.kafka_config import kafka_config
from ..utils.logging import get_structured_logger

logger = logging.getLogger(__name__)
structured_logger = get_structured_logger()


def to_isoformat(value: Optional[Any]) -> Optional[str]:
    """Convert datetime or ISO string to ISO format safely."""
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = isoparse(value)
        except Exception:
            return value  # leave as string if parsing fails
    return value.isoformat()


class KafkaService:
    """Service class for handling Kafka operations."""

    def __init__(self):
        self._producer: Optional[AIOKafkaProducer] = None
        self._initialized = False

    async def initialize(self):
        """Initialize the Kafka producer."""
        if self._initialized:
            return

        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=kafka_config.get_bootstrap_servers_list(),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                enable_idempotence=True,
                acks="all",
                retry_backoff_ms=kafka_config.kafka_retry_backoff_ms,
                request_timeout_ms=30000
            )
            await self._producer.start()
            self._initialized = True
            logger.info("Kafka producer initialized successfully")
            structured_logger.log_kafka_connection_status(
                status="connected",
                details={
                    "bootstrap_servers": kafka_config.get_bootstrap_servers_list(),
                    "topics": [
                        kafka_config.task_events_topic,
                        kafka_config.reminders_topic,
                        kafka_config.task_updates_topic
                    ]
                }
            )
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to initialize Kafka producer: {error_msg}")
            structured_logger.log_kafka_connection_status(
                status="failed",
                details={"error": error_msg}
            )
            self._initialized = False  # Continue without Kafka

    async def close(self):
        """Close the Kafka producer."""
        if self._producer:
            try:
                await self._producer.stop()
                self._initialized = False
            except Exception as e:
                logger.error(f"Error closing Kafka producer: {str(e)}")

    async def publish_event(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """Publish an event to the specified topic."""
        if not self._initialized or not kafka_config.enabled:
            logger.debug(f"Kafka disabled or not initialized. Skipping event to topic '{topic}'")
            return False

        try:
            if 'timestamp' not in event_data:
                event_data['timestamp'] = datetime.utcnow().isoformat()

            await self._producer.send_and_wait(topic, event_data)
            logger.debug(f"Event published to topic '{topic}': {event_data.get('event_type', 'unknown')}")

            structured_logger.log_kafka_event_published(
                topic=topic,
                event_type=event_data.get('event_type', 'unknown'),
                task_id=event_data.get('task_id'),
                user_id=event_data.get('user_id')
            )
            return True
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to publish event to topic '{topic}': {error_msg}", exc_info=True)
            structured_logger.log_kafka_event_failed(
                topic=topic,
                event_type=event_data.get('event_type', 'unknown'),
                error_message=error_msg
            )
            return True  # Attempt was made

    async def publish_task_event(self, event_type: str, task_data: Dict[str, Any]) -> bool:
        """Publish a task-related event."""
        event_payload = {
            'event_type': event_type,
            'task_id': task_data.get('id'),
            'user_id': str(task_data.get('user_id')),
            'title': task_data.get('title'),
            'priority': task_data.get('priority', 'medium'),
            'due_date': to_isoformat(task_data.get('due_date')),
            'reminder_at': to_isoformat(task_data.get('reminder_at')),
            'tags': task_data.get('tags', []),
            'is_completed': task_data.get('is_completed', False),
            'timestamp': datetime.utcnow().isoformat()
        }

        topic = kafka_config.task_events_topic
        return await self.publish_event(topic, event_payload)

    async def publish_reminder_event(self, task_data: Dict[str, Any]) -> bool:
        """Publish a reminder event."""
        if not task_data.get('reminder_at'):
            logger.debug("No reminder_at found, skipping reminder event")
            return False

        event_payload = {
            'event_type': 'reminder.set',
            'task_id': task_data.get('id'),
            'user_id': str(task_data.get('user_id')),
            'reminder_at': to_isoformat(task_data.get('reminder_at')),
            'due_date': to_isoformat(task_data.get('due_date')),
            'title': task_data.get('title')
        }

        topic = kafka_config.reminders_topic
        return await self.publish_event(topic, event_payload)

    async def publish_ui_sync_event(self, event_type: str, task_data: Dict[str, Any]) -> bool:
        """Publish a UI synchronization event."""
        event_payload = {
            'event_type': f'task.{event_type}',
            'task_id': task_data.get('id'),
            'user_id': str(task_data.get('user_id')),
            'action': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'payload': {
                'id': task_data.get('id'),
                'title': task_data.get('title'),
                'is_completed': task_data.get('is_completed', False),
                'due_date': to_isoformat(task_data.get('due_date')),
                'updated_at': to_isoformat(task_data.get('updated_at'))
            }
        }

        topic = kafka_config.task_updates_topic
        return await self.publish_event(topic, event_payload)


# Global instance
kafka_service = KafkaService()
