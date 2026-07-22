from app.db.models.device_config import DeviceConfig
from app.repositories.device_config_repository import DeviceConfigRepository

class DeviceConfigService:
    def __init__(self, repository: DeviceConfigRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()
    
    async def create(self, config: DeviceConfig):
        return await self.repository.add(config)