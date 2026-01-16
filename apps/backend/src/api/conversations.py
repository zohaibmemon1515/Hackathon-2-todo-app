"""
Conversation management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from pydantic import BaseModel
from ..services.conversation_service import ConversationService
from ..database.database import get_session
from ..utils.auth import get_current_user


router = APIRouter(prefix="/api", tags=["conversations"])


class ConversationResponse(BaseModel):
    id: int
    user_id: str
    title: str
    created_at: str
    updated_at: str


@router.get("/conversations", response_model=List[ConversationResponse])
def get_user_conversations(user_id: str, current_user: dict = Depends(get_current_user), db_session: Session = Depends(get_session)):
    """Get all conversations for a specific user."""
    # Verify that the requesting user has access to these conversations
    from ..utils.auth import require_user_access
    if not require_user_access(current_user.get("user_id") or current_user.get("sub"), user_id):
        raise HTTPException(status_code=403, detail="Access denied: Cannot access another user's conversations")

    try:
        conversation_service = ConversationService()
        conversations = conversation_service.get_user_conversations(db_session, user_id)

        return [
            ConversationResponse(
                id=conv.id,
                user_id=conv.user_id,
                title=conv.title or f"Conversation {conv.id}",
                created_at=conv.created_at.isoformat(),
                updated_at=conv.updated_at.isoformat()
            )
            for conv in conversations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: int, current_user: dict = Depends(get_current_user), db_session: Session = Depends(get_session)):
    """Get details of a specific conversation."""
    try:
        conversation_service = ConversationService()
        conversation = conversation_service.get_conversation(db_session, conversation_id)

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Verify that the requesting user has access to this conversation
        from ..utils.auth import require_user_access
        user_id = current_user.get("user_id") or current_user.get("sub")
        if not require_user_access(user_id, conversation.user_id):
            raise HTTPException(status_code=403, detail="Access denied: Cannot access another user's conversation")

        return ConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title or f"Conversation {conversation.id}",
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversation: {str(e)}")