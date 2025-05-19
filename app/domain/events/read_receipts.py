from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class MessageReadEvent(BaseEvent):
    message_oid: str
    reader_oid: str