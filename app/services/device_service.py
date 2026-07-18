from app.db.models.device import Device
from app.repositories.device_repository import DeviceRepository

class DeviceService:
    def __init__(self, repository: DeviceRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()
    
    async def create(self, device: Device):
        return await self.repository.add(device)