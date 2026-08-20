from uuid import UUID

from fastapi import HTTPException, status

from app.db.models.base import DeviceTypeEnum, ProtectTypeEnum
from app.db.models.device_variable import DeviceVariable
from app.repositories.device_variable_repository import DeviceVariableRepository
from app.repositories.device_repository import DeviceRepository
from app.schemas.device_variable_dto import (
    DeviceVariableCreate,
    DeviceVariableUpdate,
)


class DeviceVariableService:
    def __init__(
        self,
        repository: DeviceVariableRepository,
        device_repository: DeviceRepository,
    ):
        self.repository = repository
        self.device_repository = device_repository

    async def get_all(self):
        return await self.repository.get_all()

    async def get_by_device(self, device_id: UUID):
        await self._get_device(device_id)
        return await self.repository.get_by_device(device_id)

    async def get_by_id(self, device_id: UUID, variable_id: UUID):
        await self._get_device(device_id)
        return await self.repository.get_by_device_and_id(device_id, variable_id)

    async def create(self, device_id: UUID, dto: DeviceVariableCreate):
        device = await self._get_device(device_id)
        self._validate_device(device)

        if await self.repository.exists_duplicate(
            device_id,
            dto.name,
            dto.alias,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A variable with the same name and alias already exists for this device",
            )

        data = dto.model_dump()
        data["device_id"] = device_id

        variable = DeviceVariable(**data)
        return await self.repository.create(variable)

    async def update(
        self,
        device_id: UUID,
        variable_id: UUID,
        dto: DeviceVariableUpdate,
    ):
        variable = await self.repository.get_by_device_and_id(
            device_id,
            variable_id,
        )

        if variable is None:
            return None

        data = dto.model_dump(exclude_unset=True)

        name = data.get("name", variable.name)
        alias = data.get("alias", variable.alias)

        if await self.repository.exists_duplicate(
            device_id,
            name,
            alias,
            exclude_id=variable_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A variable with the same name and alias already exists for this device",
            )

        for key, value in data.items():
            setattr(variable, key, value)

        return await self.repository.update(variable)

    async def delete(self, device_id: UUID, variable_id: UUID) -> bool:
        variable = await self.repository.get_by_device_and_id(
            device_id,
            variable_id,
        )

        if variable is None:
            return False

        await self.repository.delete(variable)
        return True

    async def _get_device(self, device_id: UUID):
        device = await self.device_repository.get_by_id(device_id)

        if device is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        return device

    @staticmethod
    def _validate_device(device):
        if device.device_type_enum != DeviceTypeEnum.Device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device variables can only belong to a device, not a group",
            )
