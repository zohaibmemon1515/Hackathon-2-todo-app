"""
Message service for managing message entities
Provides CRUD operations for Message model
"""
from typing import List, Optional
from sqlmodel import Session, select
from ..models.message import Message, MessageBase


class MessageService:
    """Service class for handling message operations."""

    def create_message(self, db_session: Session, message_data: MessageBase) -> Message:
        """Create a new message."""
        # Extract all attributes safely
        original_content = getattr(message_data, 'original_content', None)
        processed_content = getattr(message_data, 'processed_content', None)
        language_detected = getattr(message_data, 'language_detected', None)
        command_metadata = getattr(message_data, 'command_metadata', '{}')
        extra_info = getattr(message_data, 'extra_info', '{}')

        message = Message(
            user_id=message_data.user_id,
            conversation_id=message_data.conversation_id,
            role=message_data.role,
            content=message_data.content,
            original_content=original_content,
            processed_content=processed_content,
            language_detected=language_detected,
            command_metadata=command_metadata,
            extra_info=extra_info
        )
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        return message

    def get_message(self, db_session: Session, message_id: int) -> Optional[Message]:
        """Retrieve a message by ID."""
        statement = select(Message).where(Message.id == message_id)
        return db_session.exec(statement).first()

    def get_messages_by_conversation(self, db_session: Session, conversation_id: int) -> List[Message]:
        """Retrieve all messages for a specific conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc())
        return db_session.exec(statement).all()

    def get_messages_by_user(self, db_session: Session, user_id: str) -> List[Message]:
        """Retrieve all messages for a specific user."""
        statement = select(Message).where(Message.user_id == user_id).order_by(Message.timestamp.asc())
        return db_session.exec(statement).all()

    def update_message(self, db_session: Session, message_id: int, message_data: MessageBase) -> Optional[Message]:
        """Update an existing message."""
        message = self.get_message(db_session, message_id)
        if message:
            for key, value in message_data.dict().items():
                if hasattr(message, key):
                    setattr(message, key, value)
            db_session.add(message)
            db_session.commit()
            db_session.refresh(message)
        return message

    def delete_message(self, db_session: Session, message_id: int) -> bool:
        """Delete a message by ID."""
        message = self.get_message(db_session, message_id)
        if message:
            db_session.delete(message)
            db_session.commit()
            return True
        return False