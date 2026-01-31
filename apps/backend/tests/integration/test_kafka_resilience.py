"""Integration tests for Kafka resilience.

These tests verify that core functionality works when Kafka is unavailable,
ensuring that event publishing failures don't break the main application.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from sqlmodel import Session
from datetime import datetime
from uuid import uuid4

from src.models.task import TaskCreate, TaskUpdate
from src.services.task_service import create_task, update_task, delete_task
from src.services.kafka_service import kafka_service


@pytest.mark.asyncio
async def test_create_task_when_kafka_unavailable(db_session: Session):
    """Test that task creation still works when Kafka is unavailable."""
    # Mock the Kafka service to simulate failure
    with patch.object(kafka_service, 'publish_task_event', new_callable=AsyncMock) as mock_publish:
        mock_publish.side_effect = Exception("Kafka unavailable")

        # Create test user ID
        user_id = uuid4()

        # Create task data
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            priority="medium",
            due_date=datetime(2024, 12, 31)
        )

        # This should still work despite Kafka failure
        result = await create_task(db_session, user_id, task_data)

        # Verify task was created successfully
        assert result is not None
        assert result.title == "Test Task"
        assert result.description == "Test Description"

        # Verify Kafka publishing was attempted
        assert mock_publish.called


@pytest.mark.asyncio
async def test_update_task_when_kafka_unavailable(db_session: Session):
    """Test that task updates still work when Kafka is unavailable."""
    # First create a task normally
    user_id = uuid4()
    task_data = TaskCreate(
        title="Original Task",
        description="Original Description",
        priority="medium"
    )
    created_task = await create_task(db_session, user_id, task_data)
    assert created_task is not None

    # Now mock Kafka failure during update
    with patch.object(kafka_service, 'publish_task_event', new_callable=AsyncMock) as mock_publish:
        mock_publish.side_effect = Exception("Kafka unavailable")

        # Update the task
        update_data = TaskUpdate(
            title="Updated Task",
            description="Updated Description"
        )
        result = await update_task(db_session, created_task.id, user_id, update_data)

        # Verify task was updated successfully
        assert result is not None
        assert result.title == "Updated Task"
        assert result.description == "Updated Description"

        # Verify Kafka publishing was attempted
        assert mock_publish.called


@pytest.mark.asyncio
async def test_delete_task_when_kafka_unavailable(db_session: Session):
    """Test that task deletion still works when Kafka is unavailable."""
    # First create a task normally
    user_id = uuid4()
    task_data = TaskCreate(
        title="Task to Delete",
        description="Description",
        priority="medium"
    )
    created_task = await create_task(db_session, user_id, task_data)
    assert created_task is not None

    # Now mock Kafka failure during deletion
    with patch.object(kafka_service, 'publish_task_event', new_callable=AsyncMock) as mock_publish:
        mock_publish.side_effect = Exception("Kafka unavailable")

        # Delete the task
        result = await delete_task(db_session, created_task.id, user_id)

        # Verify task was deleted successfully
        assert result is True

        # Verify Kafka publishing was attempted
        assert mock_publish.called


@pytest.mark.asyncio
async def test_multiple_kafka_failures_still_allow_operations(db_session: Session):
    """Test that multiple consecutive Kafka failures don't prevent operations."""
    user_id = uuid4()

    # Mock multiple Kafka methods to fail
    with patch.multiple(kafka_service,
                        publish_task_event=AsyncMock(side_effect=Exception("Kafka unavailable")),
                        publish_ui_sync_event=AsyncMock(side_effect=Exception("Kafka unavailable")),
                        publish_reminder_event=AsyncMock(side_effect=Exception("Kafka unavailable"))):

        # Create multiple tasks - all should succeed despite Kafka failures
        for i in range(3):
            task_data = TaskCreate(
                title=f"Test Task {i}",
                description=f"Test Description {i}",
                priority="medium"
            )
            result = await create_task(db_session, user_id, task_data)
            assert result is not None
            assert result.title == f"Test Task {i}"

        # Update a task - should succeed despite Kafka failures
        update_data = TaskUpdate(title="Updated Task")
        update_result = await update_task(db_session, 1, user_id, update_data)
        assert update_result is not None
        assert update_result.title == "Updated Task"

        # Delete a task - should succeed despite Kafka failures
        delete_result = await delete_task(db_session, 1, user_id)
        assert delete_result is True


@pytest.mark.asyncio
async def test_kafka_service_initialization_failure_is_handled_gracefully():
    """Test that Kafka service gracefully handles initialization failures."""
    # Create a new Kafka service instance to test initialization
    from src.services.kafka_service import KafkaService

    # Mock the AIOKafkaProducer to fail during initialization
    with patch('src.services.kafka_service.AIOKafkaProducer') as mock_producer_class:
        mock_producer = AsyncMock()
        mock_producer.start.side_effect = Exception("Connection refused")
        mock_producer_class.return_value = mock_producer

        service = KafkaService()
        await service.initialize()

        # Service should handle the failure gracefully
        # and continue operating (even though it won't be able to publish)
        assert service._initialized is False


def test_kafka_disabled_flag_prevents_publishing():
    """Test that disabling Kafka prevents event publishing."""
    from src.config.kafka_config import kafka_config
    from src.services.kafka_service import KafkaService

    # Temporarily disable Kafka
    original_enabled = kafka_config.enabled
    kafka_config.enabled = False

    try:
        service = KafkaService()
        # Initialize with Kafka disabled
        result = asyncio.run(service.publish_event("test-topic", {"test": "data"}))

        # Should return False when Kafka is disabled
        assert result is False
    finally:
        # Restore original setting
        kafka_config.enabled = original_enabled