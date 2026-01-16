from typing import Dict, Any, Optional, Union
from sqlmodel import Session
from datetime import datetime
import json
from sqlalchemy import insert

from ..models.conversation import Conversation
from ..models.message import Message
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService

# ✅ IMPORTANT: class AgentService hatao
# ❌ from ..services.agent_service import AgentService
# ✅ direct function import karo
from ..services.agent_service import process_request


class ChatService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.conversation_service = ConversationService()
        self.message_service = MessageService()

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[Union[str, int]] = None,
    ) -> Dict[str, Any]:

        # -------------------------------------------------
        # 1. Get or create conversation
        # -------------------------------------------------
        conversation = None

        if conversation_id and str(conversation_id).lower() != "null":
            try:
                conversation = self.conversation_service.get_conversation(
                    self.db_session, int(conversation_id)
                )
            except Exception:
                conversation = None

        if not conversation:
            conversation = self.conversation_service.create_conversation(
                self.db_session,
                Conversation(user_id=user_id, title=message[:50]),
            )

        # -------------------------------------------------
        # 2. SAVE USER MESSAGE (Direct SQL insert)
        # -------------------------------------------------
        user_stmt = (
            insert(Message)
            .values(
                user_id=user_id,
                conversation_id=conversation.id,
                role="user",
                content=message,
                extra_info="{}",  # MUST be string
                timestamp=datetime.utcnow(),
            )
            .returning(Message.id)
        )

        user_msg_id = self.db_session.execute(user_stmt).scalar()

        # -------------------------------------------------
        # 3. AI AGENT (DIRECT FUNCTION CALL)
        # -------------------------------------------------
        agent_response = await process_request(
            user_id=user_id,
            message=message,
            conversation_id=conversation.id,
        )

        response_text = agent_response.get(
            "response", "I'm sorry, I couldn't process that."
        )

        # -------------------------------------------------
        # 4. SAVE AGENT MESSAGE (Direct SQL insert)
        # -------------------------------------------------
        agent_metadata = agent_response.get("metadata", {})

        agent_stmt = (
            insert(Message)
            .values(
                user_id="system",
                conversation_id=conversation.id,
                role="assistant",
                content=response_text,
                extra_info=json.dumps(agent_metadata) if agent_metadata else "{}",
                timestamp=datetime.utcnow(),
            )
            .returning(Message.id)
        )

        agent_msg_id = self.db_session.execute(agent_stmt).scalar()

        # -------------------------------------------------
        # 5. Update conversation timestamp
        # -------------------------------------------------
        conversation.updated_at = datetime.utcnow()
        self.db_session.add(conversation)
        self.db_session.commit()

        return {
            "success": True,
            "response": response_text,
            "conversation_id": str(conversation.id),
            "message_id": str(agent_msg_id),
        }

    # -------------------------------------------------
    # READ METHODS
    # -------------------------------------------------
    def get_conversation_history(self, conversation_id: int) -> list:
        messages = self.message_service.get_messages_by_conversation(
            self.db_session, conversation_id
        )
        return [msg.model_dump(by_alias=True) for msg in messages]

    def get_user_conversations(self, user_id: str) -> list:
        conversations = self.conversation_service.get_user_conversations(
            self.db_session, user_id
        )
        return [conv.model_dump() for conv in conversations]
