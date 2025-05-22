from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.messages import Message
from infrastructure.database.models.message import MessageModel
from sqlalchemy import select, update

from infrastructure.database.models.read_receipt import ReadReceiptModel


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, message: Message):
        db_message = MessageModel.from_entity(message)
        self.session.add(db_message)
        await self.session.flush()

    # -> list[MessageModel]
    async def get_by_chat(self, chat_id: str):
        result = await self.session.execute(
            select(MessageModel).where(MessageModel.chat_id == chat_id)
        )
        return result.scalars().all()

    async def mark_as_read(self, message_id: str, reader_id: str):
        stmt = (
            update(ReadReceiptModel)
            .where(
                ReadReceiptModel.message_id == message_id,
                ReadReceiptModel.user_id == reader_id
            )
            .values(read_at=datetime.utcnow())
        )
        await self.session.execute(stmt)
        await self.session.flush()
