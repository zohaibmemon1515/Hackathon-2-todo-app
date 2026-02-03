"""
Conversation service for managing conversation entities
Provides CRUD operations for Conversation model
"""
from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationBase
import json


class ConversationService:
    """Service class for handling conversation operations."""

    def create_conversation(self, db_session: Session, conversation_data: ConversationBase) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=conversation_data.user_id,
            title=conversation_data.title,
            metadata=getattr(conversation_data, 'metadata', '{}'),
            active_context=getattr(conversation_data, 'active_context', '{}')
        )
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
        return conversation

    def get_conversation(self, db_session: Session, conversation_id: int) -> Optional[Conversation]:
        """Retrieve a conversation by ID."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return db_session.exec(statement).first()

    def get_user_conversations(self, db_session: Session, user_id: str) -> List[Conversation]:
        """Retrieve all conversations for a specific user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return db_session.exec(statement).all()

    def update_conversation(self, db_session: Session, conversation_id: int, conversation_data: ConversationBase) -> Optional[Conversation]:
        """Update an existing conversation."""
        conversation = self.get_conversation(db_session, conversation_id)
        if conversation:
            # Handle potential updates to metadata and active_context
            for key, value in conversation_data.dict().items():
                if hasattr(conversation, key):
                    setattr(conversation, key, value)
            conversation.updated_at = datetime.utcnow()
            db_session.add(conversation)
            db_session.commit()
            db_session.refresh(conversation)
        return conversation

    def update_conversation_context(self, db_session: Session, conversation_id: int, context_updates: dict) -> Optional[Conversation]:
        """Update the active context for a conversation."""
        conversation = self.get_conversation(db_session, conversation_id)
        if conversation:
            import json
            current_context = conversation.parsed_active_context
            current_context.update(context_updates)
            conversation.active_context = json.dumps(current_context)
            conversation.updated_at = datetime.utcnow()
            db_session.add(conversation)
            db_session.commit()
            db_session.refresh(conversation)
        return conversation

    def get_conversation_context(self, db_session: Session, conversation_id: int) -> dict:
        """Get the active context for a conversation."""
        conversation = self.get_conversation(db_session, conversation_id)
        if conversation:
            return conversation.parsed_active_context
        return {}

    def delete_conversation(self, db_session: Session, conversation_id: int) -> bool:
        """Delete a conversation by ID."""
        conversation = self.get_conversation(db_session, conversation_id)
        if conversation:
            db_session.delete(conversation)
            db_session.commit()
            return True
        return False