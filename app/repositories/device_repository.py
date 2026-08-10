from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.device import Device
from app.repositories.repository import Repository


class DeviceRepository(Repository[Device]):

    def __init__(self, db):
        super().__init__(db, Device)

    async def get_by_id(
        self,
        device_id: UUID,
    ) -> Device | None:

        result = await self.db.execute(
            select(Device)
            .where(Device.id == device_id)
            .options(
                selectinload(Device.driver),
                selectinload(Device.device_configs),
                selectinload(Device.device_variables),
                selectinload(Device.children),
                selectinload(Device.parent),
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
    ) -> list[Device]:

        result = await self.db.execute(
            select(Device)
            .options(
                selectinload(Device.driver),
                selectinload(Device.device_configs),
                selectinload(Device.device_variables),
                selectinload(Device.children),
                selectinload(Device.parent),
            )
            .order_by(
                Device.index,
                Device.device_name,
            )
        )

        return list(result.scalars().unique().all())

    async def get_children(
        self,
        device_id: UUID,
    ) -> list[Device]:

        result = await self.db.execute(
            select(Device)
            .where(
                Device.parent_id == device_id
            )
        )

        return list(result.scalars().all())

    async def exists(
        self,
        device_id: UUID,
    ) -> bool:

        result = await self.db.execute(
            select(Device.id)
            .where(Device.id == device_id)
        )

        return result.scalar_one_or_none() is not None