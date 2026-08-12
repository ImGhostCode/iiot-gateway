from sqlalchemy import select

from app.db.models.device_config import DeviceConfig
from app.repositories.repository import Repository


class DeviceConfigRepository(
    Repository[DeviceConfig]
):

    def __init__(self, db):

        super().__init__(
            db,
            DeviceConfig,
        )

    async def get_by_device(
        self,
        device_id,
    ):

        result = await self.db.execute(

            select(DeviceConfig)
            .where(
                DeviceConfig.device_id == device_id
            )
            .order_by(
                DeviceConfig.device_config_name
            )

        )

        return result.scalars().all()

    async def get_by_device_and_id(
        self,
        device_id,
        config_id,
    ):

        result = await self.db.execute(

            select(DeviceConfig)
            .where(
                DeviceConfig.device_id == device_id,
                DeviceConfig.id == config_id,
            )

        )

        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        device_id,
        name,
    ):

        result = await self.db.execute(

            select(DeviceConfig)
            .where(
                DeviceConfig.device_id == device_id,
                DeviceConfig.device_config_name == name,
            )

        )

        return result.scalar_one_or_none()