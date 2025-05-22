from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.values.messages import Text


@dataclass(eq=False)
class Message(BaseEntity):
    chat_id: str
    sender_id: str
    text: Text
    timestamp: datetime = field(default_factory=datetime.utcnow)
    is_read: bool = False
