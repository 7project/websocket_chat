from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class MessageCreateSchema(BaseModel):
    chat_id: str
    text: str
    sender_id: str
    timestamp: Optional[datetime] = None


class MessageReadSchema(BaseModel):
    id: str
    chat_id: str
    sender_id: str
    text: str
    timestamp: datetime
    is_read: bool

    model_config = ConfigDict(from_attributes=True)
