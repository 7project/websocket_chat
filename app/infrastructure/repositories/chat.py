from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities.chats import Chat
from infrastructure.database.models.chat import ChatModel, GroupChatModel


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, chat: Chat):
        db_chat = ChatModel.from_entity(chat)
        self.session.add(db_chat)
        await self.session.flush()

    async def get_by_id(self, chat_id: str) -> ChatModel:
        result = await self.session.execute(
            select(ChatModel).where(ChatModel.id == chat_id)
        )
        return result.scalars().first()

    async def get_group_chats(self):
        result = await self.session.execute(select(GroupChatModel))
        return result.scalars().all()