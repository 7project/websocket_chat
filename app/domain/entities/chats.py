from abc import ABC
from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.events.chats import ChatParticipantAddedEvent
from domain.values.chats import ChatType, ChatTitle
from domain.entities.messages import Message


@dataclass(eq=False)
class Chat(BaseEntity, ABC):
    title: ChatTitle
    chat_type: ChatType
    messages: set[Message] = field(default_factory=set)


@dataclass(eq=False)
class PrivateChat(Chat):
    pass


@dataclass(eq=False)
class GroupChat(Chat):
    participants: set[str] = field(default_factory=set)

    def add_participant(self, user_oid: str):
        if user_oid not in self.participants:
            self.participants.add(user_oid)
            self.register_event(ChatParticipantAddedEvent(chat_oid=self.oid, user_oid=user_oid))