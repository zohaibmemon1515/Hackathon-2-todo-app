from typing import Dict, Any, Optional, Union
from sqlmodel import Session
from datetime import datetime
import json
from sqlalchemy import insert

from ..models.conversation import Conversation
from ..models.message import Message
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
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
        # UUID ke liye Union[str, Any] rakha hai
        conversation_id: Optional[Union[str, Any]] = None,
        user_preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        # -------------------------------------------------
        # 1. Get or create conversation
        # -------------------------------------------------
        conversation = None

        # FIX: UUID string hoti hai, isliye int() hata diya gaya hai
        if conversation_id and str(conversation_id).lower() != "null":
            try:
                conversation = self.conversation_service.get_conversation(
                    self.db_session, conversation_id
                )
            except Exception as e:
                print(f"Conversation fetch error: {e}")
                conversation = None

        if not conversation:
            # Create new conversation if not found
            conversation_data = Conversation(
                user_id=user_id,
                title=message[:50],
                metadata=json.dumps(user_preferences) if user_preferences else "{}"
            )
            conversation = self.conversation_service.create_conversation(
                self.db_session,
                conversation_data,
            )

        # -------------------------------------------------
        # 2. SAVE USER MESSAGE
        # -------------------------------------------------
        from ..utils.language_detection import detect_and_process_language
        lang_analysis = detect_and_process_language(message)

        user_message_data = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role="user",
            content=message,
            original_content=message if lang_analysis['is_translated'] else None,
            processed_content=lang_analysis['processed_text'] if lang_analysis['is_translated'] else None,
            language_detected=lang_analysis['language'],
            command_metadata="{}",
            extra_info="{}"
        )

        user_message = self.message_service.create_message(self.db_session, user_message_data)
        user_msg_id = user_message.id

        # -------------------------------------------------
        # 3. AI AGENT CALL
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
        # 4. SAVE AGENT MESSAGE
        # -------------------------------------------------
        agent_metadata = agent_response.get("metadata", {})

        agent_message_data = Message(
            user_id="system",
            conversation_id=conversation.id,
            role="assistant",
            content=response_text,
            original_content=None,
            processed_content=None,
            language_detected=None,
            command_metadata="{}",
            # json.dumps ab hamesha work karega kyunki import top par hai
            extra_info=json.dumps(agent_metadata) if agent_metadata else "{}"
        )

        agent_message = self.message_service.create_message(self.db_session, agent_message_data)
        agent_msg_id = agent_message.id

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
    def get_conversation_history(self, conversation_id: Any) -> list:
        # UUID ke liye int() conversion hata di gayi hai
        messages = self.message_service.get_messages_by_conversation(
            self.db_session, conversation_id
        )
        return [msg.model_dump(by_alias=True) for msg in messages]

    def get_user_conversations(self, user_id: str) -> list:
        conversations = self.conversation_service.get_user_conversations(
            self.db_session, user_id
        )
        return [conv.model_dump() for conv in conversations]