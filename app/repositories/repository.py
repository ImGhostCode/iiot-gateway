from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class Repository(Generic[T]):
    def __init__(self, db: AsyncSession, model: type[T]):
        self.db = db
        self.model = model
    
    async def get(self, id):
        return await self.db.get(self.model, id)
    
    async def get_all(self):
        result = await self.db.execute(select(self.model))
        return result.scalars().all()
    
    async def create(self, entity: T):
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def update(self, entity: T):
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
        
    async def delete(self, entity: T):
        await self.db.delete(entity)
        await self.db.commit()


