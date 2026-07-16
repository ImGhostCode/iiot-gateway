from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.device import Device
from app.repositories.repository import Repository

class DeviceRepository(Repository[Device]):
    def __init__(self, db):
        super().__init__(db, Device)