from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.user import User
from app.repositories.repository import Repository

class UserRepository(Repository[User]):
    def __init__(self, db):
        super().__init__(db, User)

    async def get_by_id(self, id: str):
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()