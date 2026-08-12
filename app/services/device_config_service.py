import json
import uuid

from fastapi import HTTPException
from sqlalchemy import select

from app.db.models.device import Device
from app.db.models.device_config import DeviceConfig

from app.plugins.config import ConfigParameter

from app.repositories.device_config_repository import (
    DeviceConfigRepository,
)

from app.schemas.device_config_dto import (
    DeviceConfigCreate,
    DeviceConfigUpdate,
)


class DeviceConfigService:

    def __init__(
        self,
        repository: DeviceConfigRepository,
    ):

        self.repository = repository

    async def get_all(self):

        return await self.repository.get_all()

    async def get_by_device(
        self,
        device_id,
    ):

        return await self.repository.get_by_device(
            device_id
        )

    async def get_by_id(
        self,
        device_id,
        config_id,
    ):

        return await self.repository.get_by_device_and_id(
            device_id,
            config_id,
        )

    async def create(
        self,
        device_id,
        dto: DeviceConfigCreate,
    ):

        existing = await self.repository.get_by_name(
            device_id,
            dto.device_config_name,
        )

        if existing:

            raise HTTPException(
                status_code=409,
                detail=(
                    f"Config '{dto.device_config_name}' "
                    "already exists"
                ),
            )

        config = DeviceConfig(

            device_config_name=dto.device_config_name,

            data_side=dto.data_side,

            description=dto.description,

            value=dto.value,

            enum_info=dto.enum_info,

            device_id=device_id,

        )

        return await self.repository.create(
            config
        )

    async def update(
        self,
        device_id,
        config_id,
        dto: DeviceConfigUpdate,
    ):

        config = await self.repository.get_by_device_and_id(
            device_id,
            config_id,
        )

        if config is None:

            return None

        data = dto.model_dump(
            exclude_unset=True
        )

        if (
            "device_config_name" in data
            and
            data["device_config_name"]
            != config.device_config_name
        ):

            existing = await self.repository.get_by_name(
                device_id,
                data["device_config_name"],
            )

            if existing:

                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Config "
                        f"'{data['device_config_name']}' "
                        "already exists"
                    ),
                )

        for key, value in data.items():

            setattr(
                config,
                key,
                value,
            )

        return await self.repository.update(
            config
        )

    async def delete(
        self,
        device_id,
        config_id,
    ):

        config = await self.repository.get_by_device_and_id(
            device_id,
            config_id,
        )

        if config is None:

            return False

        await self.repository.delete(
            config
        )

        return True

    async def ensure_defaults(
        self,
        device: Device,
        driver_cls,
    ):

        schema = driver_cls.config_schema()

        created = []

        for parameter in schema:

            existing = await self.repository.get_by_name(
                device.id,
                parameter.name,
            )

            if existing:

                continue

            config = DeviceConfig(

                device_config_name=parameter.name,

                data_side=parameter.data_side,

                description=parameter.description,

                value=parameter.default,

                enum_info=parameter.enum_info,

                device_id=device.id,

            )

            await self.repository.create(
                config
            )

            created.append(config)

        return created