"""
Chat API endpoint for AI-powered conversation
Handles natural language todo management and conversation history.
"""
from fastapi import APIRouter, Depends, HTTPException, Request # 1. Request import karein
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlmodel import Session
from typing import Dict, Any, Optional, Union
from pydantic import BaseModel, Field
import html
import re
import json

# Services & Database Imports
from ..services.chat_service import ChatService
from ..database.database import get_session

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# FIX: Prefix ko khali "" kar diya kyunki main.py mein pehle hi "/api/v1" hai
# Isse path /api/v1/conversations banega na ki /api/v1/api/conversations
router = APIRouter(prefix="", tags=["chat"])

# --- MODELS ---

class ChatRequest(BaseModel):
    message: str
    # FIX: Frontend se ID string ya number dono aa sakti hain, aur null bhi
    conversation_id: Optional[Union[str, int]] = None
    user_preferences: Optional[Dict[str, Any]] = Field(default_factory=dict)  # Added for language preferences and context extensions

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    message_id: Optional[str] = None

# --- ENDPOINTS ---

@router.post("/{user_id}/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat_endpoint(
    request: Request,               # 2. SlowAPI ke liye Request object add kiya
    user_id: str,
    chat_data: ChatRequest,         # 3. Purane 'request' ka naam badal kar 'chat_data' rakha
    db_session: Session = Depends(get_session)
):
    """POST /api/v1/{user_id}/chat"""
    try:
        # 4. Ab 'chat_data.message' use karein
        sanitized_message = sanitize_input(chat_data.message)
        chat_service = ChatService(db_session)

        result = await chat_service.process_message(
            user_id=user_id,
            message=sanitized_message,
            conversation_id=chat_data.conversation_id,
            user_preferences=chat_data.user_preferences or {}
        )

        return ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            message_id=result.get("message_id")
        )
    except Exception as e:
        # Debugging ke liye error print karna achi practice hai
        print(f"Chat Endpoint Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations")
async def get_user_conversations(user_id: str, db_session: Session = Depends(get_session)):
    """GET /api/v1/conversations?user_id={user_id}"""
    try:
        chat_service = ChatService(db_session)
        conversations = chat_service.get_user_conversations(user_id)
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}")
async def get_conversation_details(conversation_id: str, db_session: Session = Depends(get_session)):
    """GET /api/v1/conversations/{conversation_id}"""
    try:
        chat_service = ChatService(db_session)
        history = chat_service.get_conversation_history(int(conversation_id))
        return {"id": conversation_id, "messages": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- UTILS ---

def sanitize_input(text: str) -> str:
    if not text: return text
    text = re.sub(r'<[^>]+>', '', text)
    text = html.escape(text)
    return text.strip()