from app.db.models.system_config import SystemConfig
from app.repositories.system_config_repository import SystemConfigRepository

from app.schemas.system_config_dto import SystemConfigCreate, SystemConfigUpdate

class SystemConfigService:
    def __init__(self, repository: SystemConfigRepository):
        self.repository = repository
        
    async def get(self) -> SystemConfig:

        config = await self.repository.get()

        if config is None:
            config = await self.repository.create_default()

        return config

    async def create_default(self) -> SystemConfig:
        return await self.repository.create_default()

    async def update(
        self,
        dto: SystemConfigUpdate,
    ) -> SystemConfig | None:

        config = await self.get()

        data = dto.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():
            setattr(config, key, value)

        return await self.repository.update(
            config
        )