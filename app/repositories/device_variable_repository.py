from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.device_variable import DeviceVariable
from app.repositories.repository import Repository

class DeviceVariableRepository(Repository[DeviceVariable]):
    def __init__(self, db):
        super().__init__(db, DeviceVariable)