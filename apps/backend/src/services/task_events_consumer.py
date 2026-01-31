"""Task Events Consumer Module

This module implements a basic consumer for the task-events topic
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


class TaskEventsConsumer:
    """Basic consumer for task-events topic that logs events."""

    def __init__(self):
        self.consumer: AIOKafkaConsumer = None
        self.running = False

    async def initialize(self):
        """Initialize the Kafka consumer."""
        try:
            self.consumer = AIOKafkaConsumer(
                kafka_config.task_events_topic,
                bootstrap_servers=kafka_config.get_bootstrap_servers_list(),
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                group_id="task-events-group",
                auto_offset_reset="earliest"
            )
            await self.consumer.start()
            logger.info(f"Task events consumer initialized and subscribed to '{kafka_config.task_events_topic}'")
        except Exception as e:
            logger.error(f"Failed to initialize task events consumer: {str(e)}")
            raise

    async def consume_events(self):
        """Consume events from the task-events topic."""
        if not self.consumer:
            logger.error("Consumer not initialized")
            return

        self.running = True
        logger.info("Starting to consume task events...")

        try:
            async for msg in self.consumer:
                try:
                    event_data = msg.value
                    logger.info(f"Received task event: {event_data.get('event_type', 'unknown')} - "
                               f"Task ID: {event_data.get('task_id', 'unknown')}")

                    # Log detailed event information
                    logger.debug(f"Full event data: {json.dumps(event_data, indent=2, default=str)}")

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON from message: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)

                if not self.running:
                    break
        except Exception as e:
            logger.error(f"Error in event consumption loop: {e}", exc_info=True)
        finally:
            logger.info("Task events consumer stopped")

    async def stop(self):
        """Stop the consumer."""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info("Task events consumer stopped")


# Global instance
task_events_consumer = TaskEventsConsumer()


async def run_task_events_consumer():
    """Run the task events consumer."""
    if not kafka_config.enabled:
        logger.info("Kafka is disabled, skipping task events consumer")
        return

    await task_events_consumer.initialize()

    def signal_handler():
        logger.info("Shutdown signal received, stopping consumer...")
        asyncio.create_task(task_events_consumer.stop())

    # Handle shutdown signals
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)

    try:
        await task_events_consumer.consume_events()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping consumer...")
    finally:
        await task_events_consumer.stop()


if __name__ == "__main__":
    # For testing purposes
    asyncio.run(run_task_events_consumer())