from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import List
import datetime

from app.database import get_db_session
from app.models.chat import ChatSession, ChatMessage

router = APIRouter()

# Pydantic model for response
class MessageResponse(BaseModel):
    id: int
    sender: str
    message: str
    timestamp: datetime.datetime

    class Config:
        orm_mode = True

@router.get("/sessions/{session_uuid}/messages", response_model=List[MessageResponse])
async def get_chat_history(
    session_uuid: UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Retrieves all messages for a given chat session.
    """
    # First, find the session to ensure it exists
    session_result = await db.execute(
        select(ChatSession).filter(ChatSession.session_uuid == session_uuid)
    )
    chat_session = session_result.scalars().first()

    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found.")

    # Then, retrieve all messages for that session, ordered by timestamp
    messages_result = await db.execute(
        select(ChatMessage)
        .filter(ChatMessage.session_id == chat_session.id)
        .order_by(ChatMessage.timestamp.asc())
    )
    messages = messages_result.scalars().all()
    
    return messages
