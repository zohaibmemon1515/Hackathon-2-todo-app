import asyncio
import signal
import sys
import os
from typing import Callable
import structlog

from .consumers.reminder_consumer import ReminderConsumer
from .utils.logger import get_logger


async def main():
    """Main entry point for the notification service."""
    logger = get_logger()
    logger.info("Starting notification service...")

    # Create and start the consumer
    consumer = ReminderConsumer()

    # Handle shutdown signals
    def signal_handler(signame: str):
        logger.info(f"Received signal {signame}, initiating graceful shutdown...")
        consumer.handle_signal(signame)

    # Register signal handlers
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler('SIGTERM'))
    signal.signal(signal.SIGINT, lambda s, f: signal_handler('SIGINT'))

    try:
        # Start the consumer
        await consumer.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
    except Exception as e:
        logger.error("Unexpected error in main", error=str(e))
        sys.exit(1)
    finally:
        await consumer.stop()
        logger.info("Notification service stopped")


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())