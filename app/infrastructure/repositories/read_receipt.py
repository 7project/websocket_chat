from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from infrastructure.database.models.read_receipt import ReadReceiptModel


class ReadReceiptRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, message_id: str, user_id: str):
        receipt = ReadReceiptModel(message_id=message_id, user_id=user_id)
        self.session.add(receipt)
        await self.session.flush()
        return receipt

    async def get_by_message(self, message_id: str):
        result = await self.session.execute(
            select(ReadReceiptModel).where(ReadReceiptModel.message_id == message_id)
        )
        return result.scalars().all()
