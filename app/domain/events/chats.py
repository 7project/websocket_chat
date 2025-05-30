from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class ChatParticipantAddedEvent(BaseEvent):
    chat_oid: str
    user_oid: str


@dataclass
class NewChatCreated(BaseEvent):
    chat_oid: str
    chat_title: str
