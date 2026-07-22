from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.device_config import DeviceConfig
from app.repositories.repository import Repository

class DeviceConfigRepository(Repository[DeviceConfig]):
    def __init__(self, db):
        super().__init__(db, DeviceConfig)