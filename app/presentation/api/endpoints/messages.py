from typing import List

from fastapi import APIRouter, Depends

from application.mediator import Mediator
from application.dependencies import get_mediator
from infrastructure.repositories.message import MessageRepository
from infrastructure.database.session import get_db
from presentation.api.schemas.message import MessageReadSchema

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/chat/{chat_id}", response_model=List[MessageReadSchema])
async def get_chat_messages(
    chat_id: str,
    db=Depends(get_db)
):
    message_repo = MessageRepository(db)
    messages = await message_repo.get_by_chat(chat_id)
    return [
        MessageReadSchema(
            id=msg.id,
            chat_id=msg.chat_id,
            sender_id=msg.sender_id,
            text=msg.text,
            timestamp=msg.timestamp,
            is_read=msg.is_read
        )
        for msg in messages
    ]
