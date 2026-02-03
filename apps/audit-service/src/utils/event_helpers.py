import json
from typing import Dict, Any, Optional
import structlog

logger = structlog.get_logger()


def deserialize_event(message_value: bytes) -> Optional[Dict[str, Any]]:
    """
    Deserialize a Kafka message value from JSON bytes to dictionary.

    Args:
        message_value: Raw bytes from Kafka message

    Returns:
        Deserialized event dictionary or None if deserialization fails
    """
    try:
        event_dict = json.loads(message_value.decode('utf-8'))
        return event_dict
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error("Failed to deserialize event", error=str(e))
        return None


def validate_task_event(event: Dict[str, Any]) -> bool:
    """
    Validate that an event is a proper task event.

    Args:
        event: Dictionary representing the event

    Returns:
        True if event is valid, False otherwise
    """
    required_fields = ['event_type', 'task_id', 'user_id', 'timestamp', 'payload']

    for field in required_fields:
        if field not in event:
            logger.error(f"Missing required field in task event: {field}")
            return False

    valid_event_types = ['task.created', 'task.updated', 'task.completed', 'task.deleted']
    if event['event_type'] not in valid_event_types:
        logger.error(f"Invalid event type for task consumer: {event['event_type']}")
        return False

    return True