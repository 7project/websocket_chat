from dataclasses import dataclass

from application.mediator import Mediator
from domain.entities.chats import GroupChat, ChatTitle
from domain.values.chats import ChatType
from infrastructure.repositories.chat import ChatRepository

from domain.events.chats import NewChatCreated


@dataclass
class CreateChatCommand:
    title: str
    creator_id: str
    participants: list[str]


@dataclass
class CreateChatCommandHandler:
    chat_repo: ChatRepository
    mediator: Mediator

    async def handle(self, command: CreateChatCommand):
        chat = GroupChat(title=ChatTitle(command.title), participants=set(command.participants), chat_type=ChatType.GROUP)
        await self.chat_repo.save(chat)
        await self.mediator.publish(
            NewChatCreated(chat_oid=chat.oid, chat_title=chat.title.as_generic_type())
        )