from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.logger import logger
from app.db.models.system_config import SystemConfig
from app.db.models.base import IoTPlatformType
from app.repositories.repository import Repository

class SystemConfigRepository:
    def __init__(self, db):
        self.db = db

    async def get(self) -> SystemConfig | None:

        result = await self.db.execute(
            select(SystemConfig)
        )

        return result.scalar_one_or_none()

    async def create_default(self):

        result = await self.get()

        if result is not None:
            return result

        config = SystemConfig(
            gateway_name = "IIoT Gateway",
            client_id = "iiot-gateway-client-id",
            mqtt_ip = "localhost",
            mqtt_port = 1883,
            mqtt_uname = "",
            mqtt_upwd = "",
            iot_platform_type = IoTPlatformType.ThingsBoard
        )

        self.db.add(config)

        await self.db.commit()

        await self.db.refresh(config)

        return config

    async def update(self, config):

        await self.db.commit()

        await self.db.refresh(config)

        return config