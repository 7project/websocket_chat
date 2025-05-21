from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infrastructure.database.models.user import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: UserModel):
        self.session.add(user)
        await self.session.flush()

    async def get_by_id(self, user_id: str) -> UserModel:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalars().first()

    async def get_by_email(self, email: str) -> UserModel:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalars().first()
