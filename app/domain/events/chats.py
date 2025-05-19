from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class ChatParticipantAddedEvent(BaseEvent):
    chat_oid: str
    user_oid: str