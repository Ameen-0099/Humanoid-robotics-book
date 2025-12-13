from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.services.logger import logger
from app.services.vector_db_service import VectorDBService
from app.services.qdrant_service import QdrantSearchService
from app.services.openai_service import OpenAIService
from app import config
from app.database import get_db_session
from app.models.chat import ChatSession, ChatMessage

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None
    session_uuid: Optional[UUID] = None

class ChatResponse(BaseModel):
    answer: str
    source_documents: List[Dict[str, Any]] = []
    session_uuid: UUID

# Dependency Injection for services
def get_vector_db_service():
    return VectorDBService()

def get_qdrant_search_service(vector_db: VectorDBService = Depends(get_vector_db_service)):
    return QdrantSearchService(vector_db)

def get_openai_service():
    return OpenAIService(api_key=config.OPENAI_API_KEY)

@router.post("/chatbot", response_model=ChatResponse)
async def ask_chatbot(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db_session),
    qdrant_service: QdrantSearchService = Depends(get_qdrant_search_service),
    openai_service: OpenAIService = Depends(get_openai_service)
) -> ChatResponse:
    if not request.question.strip():
        logger.warning("Received empty question in chatbot request.")
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        # 1. Find or create the chat session
        session_uuid = request.session_uuid
        if session_uuid:
            result = await db.execute(select(ChatSession).filter(ChatSession.session_uuid == session_uuid))
            chat_session = result.scalars().first()
            if not chat_session:
                raise HTTPException(status_code=404, detail="Chat session not found.")
        else:
            session_uuid = uuid4()
            chat_session = ChatSession(session_uuid=session_uuid)
            db.add(chat_session)
            await db.flush() # Flush to get the ID for foreign key reference

        # 2. Save user message
        user_message = ChatMessage(
            session_id=chat_session.id,
            sender='user',
            message=request.question
        )
        db.add(user_message)

        # 3. Search for relevant document chunks
        logger.info(f"Searching Qdrant for question: '{request.question}' (selected_text: {request.selected_text is not None})")
        similar_chunks = await qdrant_service.search_similar_chunks(request.question, request.selected_text)
        logger.debug(f"Found {len(similar_chunks)} similar chunks.")

        # 4. Synthesize an answer
        logger.info("Synthesizing answer using OpenAI service.")
        synthesized_answer = openai_service.synthesize_answer(
            query=request.question,
            chunks=similar_chunks,
            selected_text=request.selected_text
        )
        logger.info("Answer synthesized successfully.")

        # 5. Save bot message
        bot_message = ChatMessage(
            session_id=chat_session.id,
            sender='bot',
            message=synthesized_answer
        )
        db.add(bot_message)
        
        # 6. Commit all changes to the database
        await db.commit()

        # 7. Format the response
        return ChatResponse(
            answer=synthesized_answer,
            source_documents=similar_chunks,
            session_uuid=chat_session.session_uuid
        )
    except Exception as e:
        logger.error(f"Error in ask_chatbot endpoint: {e}", exc_info=True)
        await db.rollback() # Rollback changes on error
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing your request.")

