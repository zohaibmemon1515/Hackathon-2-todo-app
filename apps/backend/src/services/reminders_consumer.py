"""Reminders Consumer Module

This module implements a basic consumer for the reminders topic
that logs received events. This consumer runs as a background service.
"""

import asyncio
import json
import logging
from typing import Dict, Any
from aiokafka import AIOKafkaConsumer
from contextlib import asynccontextmanager
import signal

from ..config.kafka_config import kafka_config

logger = logging.getLogger(__name__)


class RemindersConsumer:
    """Basic consumer for reminders topic that logs events."""

    def __init__(self):
        self.consumer: AIOKafkaConsumer = None
        self.running = False

    async def initialize(self):
        """Initialize the Kafka consumer."""
        try:
            self.consumer = AIOKafkaConsumer(
                kafka_config.reminders_topic,
                bootstrap_servers=kafka_config.get_bootstrap_servers_list(),
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                group_id="reminders-group",
                auto_offset_reset="earliest"
            )
            await self.consumer.start()
            logger.info(f"Reminders consumer initialized and subscribed to '{kafka_config.reminders_topic}'")
        except Exception as e:
            logger.error(f"Failed to initialize reminders consumer: {str(e)}")
            raise

    async def consume_events(self):
        """Consume events from the reminders topic."""
        if not self.consumer:
            logger.error("Consumer not initialized")
            return

        self.running = True
        logger.info("Starting to consume reminder events...")

        try:
            async for msg in self.consumer:
                try:
                    event_data = msg.value
                    logger.info(f"Received reminder event: {event_data.get('event_type', 'unknown')} - "
                               f"Task ID: {event_data.get('task_id', 'unknown')} - "
                               f"Reminder at: {event_data.get('reminder_at', 'unknown')}")

                    # Log detailed event information
                    logger.debug(f"Full reminder event data: {json.dumps(event_data, indent=2, default=str)}")

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON from message: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)

                if not self.running:
                    break
        except Exception as e:
            logger.error(f"Error in reminder event consumption loop: {e}", exc_info=True)
        finally:
            logger.info("Reminders consumer stopped")

    async def stop(self):
        """Stop the consumer."""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info("Reminders consumer stopped")


# Global instance
reminders_consumer = RemindersConsumer()


async def run_reminders_consumer():
    """Run the reminders consumer."""
    if not kafka_config.enabled:
        logger.info("Kafka is disabled, skipping reminders consumer")
        return

    await reminders_consumer.initialize()

    def signal_handler():
        logger.info("Shutdown signal received, stopping consumer...")
        asyncio.create_task(reminders_consumer.stop())

    # Handle shutdown signals
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)

    try:
        await reminders_consumer.consume_events()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping consumer...")
    finally:
        await reminders_consumer.stop()


if __name__ == "__main__":
    # For testing purposes
    asyncio.run(run_reminders_consumer())