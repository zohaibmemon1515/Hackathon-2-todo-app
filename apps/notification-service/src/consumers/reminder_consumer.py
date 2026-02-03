import asyncio
from aiokafka import AIOKafkaConsumer
import json
import signal
from typing import Optional
import sys
import os
import structlog

from ..utils.event_helpers import deserialize_event, validate_reminder_event
from ..models.notification_event import NotificationEvent, NotificationLogEntry
from ..utils.logger import get_logger
from config.kafka_config import get_notification_consumer_config


class ReminderConsumer:
    def __init__(self):
        self.config = get_notification_consumer_config()
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.running = False
        self.logger = get_logger()

    async def start(self):
        """Start the reminder consumer."""
        self.running = True

        self.consumer = AIOKafkaConsumer(
            self.config.topic_name,
            bootstrap_servers=self.config.bootstrap_servers,
            group_id=self.config.group_id,
            auto_offset_reset=self.config.auto_offset_reset,
            enable_auto_commit=self.config.enable_auto_commit,
            max_poll_records=self.config.max_poll_records,
            session_timeout_ms=self.config.session_timeout_ms
        )

        await self.consumer.start()
        self.logger.info(
            "Reminder consumer started",
            bootstrap_servers=self.config.bootstrap_servers,
            group_id=self.config.group_id,
            topic=self.config.topic_name
        )

        try:
            async for msg in self.consumer:
                if not self.running:
                    break

                await self.process_message(msg)

        except Exception as e:
            self.logger.error("Error in consumer loop", error=str(e))
        finally:
            await self.stop()

    async def process_message(self, msg):
        """Process a single Kafka message."""
        try:
            event_data = deserialize_event(msg.value)
            if not event_data:
                self.logger.error("Failed to deserialize message", offset=msg.offset)
                return

            if not validate_reminder_event(event_data):
                self.logger.error(
                    "Invalid reminder event",
                    event_data=event_data,
                    offset=msg.offset
                )
                return

            notification_event = NotificationEvent(**event_data)

            await self.simulate_notification(notification_event)

            self.logger.info(
                "Processed reminder event",
                task_id=notification_event.task_id,
                user_id=str(notification_event.user_id),
                event_type=notification_event.event_type
            )

        except Exception as e:
            self.logger.error(
                "Error processing message",
                error=str(e),
                offset=msg.offset,
                raw_message=msg.value.decode("utf-8", errors="ignore")
            )
            await self.log_failed_processing(msg, str(e))

    async def simulate_notification(self, notification_event: NotificationEvent):
        """Simulate sending a notification."""
        try:
            log_entry = NotificationLogEntry(
                notification_event=notification_event,
                delivery_status="attempted"
            )

            self.logger.info(
                "Simulated notification sent",
                log_entry=log_entry.model_dump(mode="json")
            )

        except Exception as e:
            self.logger.error("Error during notification simulation", error=str(e))

            log_entry = NotificationLogEntry(
                notification_event=notification_event,
                delivery_status="failed",
                error_message=str(e)
            )

            self.logger.error(
                "Notification failed",
                log_entry=log_entry.model_dump(mode="json")
            )

    async def log_failed_processing(self, msg, error_msg: str):
        """Log when message processing fails."""
        try:
            event_data = deserialize_event(msg.value)
            if event_data and validate_reminder_event(event_data):
                notification_event = NotificationEvent(**event_data)

                log_entry = NotificationLogEntry(
                    notification_event=notification_event,
                    delivery_status="failed",
                    error_message=error_msg
                )

                self.logger.error(
                    "Failed to process reminder event",
                    log_entry=log_entry.model_dump(mode="json")
                )

        except Exception:
            self.logger.error(
                "Could not create log entry for failed message",
                offset=msg.offset,
                error=error_msg
            )

    async def stop(self):
        """Stop the consumer gracefully."""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
        self.logger.info("Reminder consumer stopped")

    def handle_signal(self, signame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signame}, shutting down...")
        self.running = False
