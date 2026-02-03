import asyncio
from aiokafka import AIOKafkaConsumer
from typing import Optional
import signal

from ..models.audit_record import TaskEvent, AuditService
from ..utils.event_helpers import deserialize_event, validate_task_event
from ..utils.logger import get_logger
from config.kafka_config import get_audit_consumer_config


class TaskEventsConsumer:
    def __init__(self):
        self.config = get_audit_consumer_config()
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.running = False
        self.logger = get_logger()
        self.audit_service = AuditService()

    async def start(self):
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
            "Task events consumer started",
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
        try:
            event_data = deserialize_event(msg.value)
            if not event_data:
                self.logger.error("Failed to deserialize message", offset=msg.offset)
                return

            # Ensure payload exists
            event_data.setdefault("payload", {})

            if not validate_task_event(event_data):
                self.logger.error("Invalid task event", event_data=event_data, offset=msg.offset)
                return

            task_event = TaskEvent(**event_data)
            await self.process_task_event(task_event)

            self.logger.info(
                "Processed task event",
                task_id=task_event.task_id,
                user_id=task_event.user_id,
                event_type=task_event.event_type
            )

        except Exception as e:
            self.logger.error(
                "Error processing message",
                error=str(e),
                raw_message=msg.value.decode("utf-8", errors="ignore")
            )
            await self.log_failed_processing(msg, str(e))

    async def process_task_event(self, task_event: TaskEvent):
        try:
            audit_record = self.audit_service.create_audit_record_from_task_event(task_event)
            self.audit_service.save_audit_record(audit_record)
            self.logger.info(
                "Audit record created and saved",
                record_id=audit_record.record_id,
                event_type=audit_record.event_type,
                task_id=audit_record.task_id
            )
        except Exception as e:
            self.logger.error(
                "Error processing task event",
                error=str(e),
                task_id=task_event.task_id,
                user_id=task_event.user_id
            )

    async def log_failed_processing(self, msg, error_msg: str):
        try:
            event_data = deserialize_event(msg.value)
            if event_data and validate_task_event(event_data):
                task_event = TaskEvent(**event_data)
                self.logger.error(
                    "Failed to process task event",
                    task_id=task_event.task_id,
                    user_id=task_event.user_id,
                    event_type=task_event.event_type,
                    error=error_msg
                )
        except Exception:
            self.logger.error("Could not log failed message processing", error=error_msg)

    async def stop(self):
        self.running = False
        if self.consumer:
            await self.consumer.stop()
        self.logger.info("Task events consumer stopped")

    def handle_signal(self, signame):
        self.logger.info(f"Received signal {signame}, shutting down...")
        self.running = False


# Run consumer with signal handling
async def main():
    consumer = TaskEventsConsumer()
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda s=sig: consumer.handle_signal(s.name))
    await consumer.start()


if __name__ == "__main__":
    asyncio.run(main())
