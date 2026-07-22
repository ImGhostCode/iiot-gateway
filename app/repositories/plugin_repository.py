from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.driver import Driver
from app.repositories.repository import Repository

class PluginRepository(Repository[Driver]):
    def __init__(self, db):
        super().__init__(db, Driver)