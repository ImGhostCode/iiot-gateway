from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.device_variable import DeviceVariable
from app.repositories.repository import Repository


class DeviceVariableRepository(Repository[DeviceVariable]):
    def __init__(self, db):
        super().__init__(db, DeviceVariable)

    async def get_all(self):
        result = await self.db.execute(
            select(DeviceVariable)
            .options(selectinload(DeviceVariable.device))
            .order_by(
                DeviceVariable.index,
                DeviceVariable.name,
            )
        )
        return result.scalars().all()

    async def get_by_device(self, device_id: UUID):
        result = await self.db.execute(
            select(DeviceVariable)
            .options(selectinload(DeviceVariable.device))
            .where(DeviceVariable.device_id == device_id)
            .order_by(
                DeviceVariable.index,
                DeviceVariable.name,
            )
        )
        return result.scalars().all()

    async def get_by_device_and_id(
        self,
        device_id: UUID,
        variable_id: UUID,
    ):
        result = await self.db.execute(
            select(DeviceVariable)
            .options(selectinload(DeviceVariable.device))
            .where(
                DeviceVariable.device_id == device_id,
                DeviceVariable.id == variable_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, variable_id: UUID):
        result = await self.db.execute(
            select(DeviceVariable)
            .options(selectinload(DeviceVariable.device))
            .where(DeviceVariable.id == variable_id)
        )
        return result.scalar_one_or_none()

    async def exists_duplicate(
        self,
        device_id: UUID,
        name: str,
        alias: str | None,
        exclude_id: UUID | None = None,
    ) -> bool:
        query = select(DeviceVariable.id).where(
            DeviceVariable.device_id == device_id,
            DeviceVariable.name == name,
        )

        if alias is not None:
            query = query.where(DeviceVariable.alias == alias)

        if exclude_id is not None:
            query = query.where(DeviceVariable.id != exclude_id)

        result = await self.db.execute(query.limit(1))
        return result.scalar_one_or_none() is not None
