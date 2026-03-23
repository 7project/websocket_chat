from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities.chats import Chat
from infrastructure.database.models.chat import ChatModel, GroupChatModel
from infrastructure.database.models.chat_participant import ChatParticipantModel


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, chat: Chat, creator_id: str = None, participants: list[str] = None):
        db_chat = ChatModel.from_entity(chat, creator_id=creator_id, participants=participants)
        self.session.add(db_chat)
        await self.session.flush()

    async def get_by_id(self, chat_id: str) -> ChatModel:
        result = await self.session.execute(
            select(ChatModel)
            .options(selectinload(ChatModel.participants))
            .where(ChatModel.id == chat_id)
        )
        return result.scalars().first()

    async def get_all(self) -> list[ChatModel]:
        result = await self.session.execute(
            select(ChatModel).options(selectinload(ChatModel.participants))
        )
        return result.scalars().all()

    async def get_group_chats(self):
        result = await self.session.execute(select(GroupChatModel))
        return result.scalars().all()

    async def add_participant(self, chat_id: str, user_id: str) -> bool:
        existing = await self.session.execute(
            select(ChatParticipantModel).where(
                ChatParticipantModel.chat_id == chat_id,
                ChatParticipantModel.user_id == user_id
            )
        )
        if existing.scalars().first():
            return False
        
        participant = ChatParticipantModel(chat_id=chat_id, user_id=user_id)
        self.session.add(participant)
        await self.session.flush()
        return True

    async def remove_participant(self, chat_id: str, user_id: str) -> bool:
        result = await self.session.execute(
            select(ChatParticipantModel).where(
                ChatParticipantModel.chat_id == chat_id,
                ChatParticipantModel.user_id == user_id
            )
        )
        participant = result.scalars().first()
        if participant:
            await self.session.delete(participant)
            await self.session.flush()
            return True
        return False

    async def get_participants(self, chat_id: str) -> list[str]:
        result = await self.session.execute(
            select(ChatParticipantModel.user_id).where(ChatParticipantModel.chat_id == chat_id)
        )
        return [row[0] for row in result.all()]