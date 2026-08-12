import json
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete

from app.db.models.base import (
    DataSide,
    DeviceTypeEnum,
)

from app.db.models.device import (
    Device,
)

from app.db.models.device_config import (
    DeviceConfig,
)

from app.repositories.device_repository import (
    DeviceRepository,
)

from app.repositories.plugin_repository import (
    PluginRepository,
)

from app.repositories.device_config_repository import (
    DeviceConfigRepository,
)


from app.schemas.device_dto import (
    DeviceCreate,
    DeviceUpdate,
)

from app.plugins.manager import (
    PluginManager,
)


class DeviceService:

    def __init__(
        self,
        repository: DeviceRepository,
        plugin_repository: PluginRepository,
        plugin_manager: PluginManager,
        config_repository: DeviceConfigRepository | None = None,
    ):

        self.repository = repository

        self.plugin_repository = (
            plugin_repository
        )

        self.config_repository = config_repository

        self.plugin_manager = (
            plugin_manager
        )

    async def get_all(self):

        return await self.repository.get_all()

    async def get_by_id(
        self,
        device_id: UUID,
    ):

        return await self.repository.get_by_id(
            device_id
        )

    async def create(
        self,
        dto: DeviceCreate,
    ):

        await self._validate_device(
            dto
        )

        device = Device(
            **dto.model_dump()
        )

        created = await self.repository.create(
            device
        )

        # Reload relationships.
        device = await self.repository.get_by_id(
            created.id
        )

        if (
            device.device_type_enum
            == DeviceTypeEnum.Device
        ):

            await self._create_driver_configs(
                device
            )

            device = (
                await self.repository
                .get_by_id(device.id)
            )

        return device

    async def update(
        self,
        device_id: UUID,
        dto: DeviceUpdate,
    ):

        device = await self.repository.get_by_id(
            device_id
        )

        if device is None:
            return None

        data = dto.model_dump(
            exclude_unset=True
        )

        driver_changed = (
            "driver_id" in data
            and data["driver_id"]
            != device.driver_id
        )

        old_type = (
            device.device_type_enum
        )

        for key, value in data.items():
            setattr(
                device,
                key,
                value,
            )

        await self._validate_existing_device(
            device
        )

        await self.repository.update(
            device
        )

        if (
            driver_changed
            and device.device_type_enum
            == DeviceTypeEnum.Device
        ):

            await self._replace_driver_configs(
                device
            )

        return await self.repository.get_by_id(
            device_id
        )

    async def delete(
        self,
        device_id: UUID,
    ) -> bool:

        device = await self.repository.get_by_id(
            device_id
        )

        if device is None:
            return False

        children = (
            await self.repository.get_children(
                device_id
            )
        )

        if (
            device.device_type_enum
            == DeviceTypeEnum.Group
            and children
        ):

            raise HTTPException(
                status_code=409,
                detail=(
                    "Group contains devices "
                    "and cannot be deleted"
                ),
            )

        await self.repository.delete(
            device
        )

        return True

    async def _validate_device(
        self,
        dto: DeviceCreate,
    ):

        if (
            dto.device_type_enum
            == DeviceTypeEnum.Device
        ):

            if dto.driver_id is None:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "A driver is required "
                        "for a device"
                    ),
                )

            driver = (
                await self.plugin_repository
                .get_by_id(dto.driver_id)
            )

            if driver is None:

                raise HTTPException(
                    status_code=400,
                    detail="Driver not found",
                )

            plugin = (
                self.plugin_manager
                .get_plugin(
                    driver.driver_name
                )
            )

            if plugin is None:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Plugin '{driver.driver_name}' "
                        "is not discovered"
                    ),
                )

        else:

            # Groups don't use a runtime driver.
            dto.driver_id = None

    async def _validate_existing_device(
        self,
        device: Device,
    ):

        if (
            device.device_type_enum
            == DeviceTypeEnum.Group
        ):

            device.driver_id = None

            return

        if device.driver_id is None:

            raise HTTPException(
                status_code=400,
                detail=(
                    "A driver is required "
                    "for a device"
                ),
            )

        driver = (
            await self.plugin_repository
            .get_by_id(
                device.driver_id
            )
        )

        if driver is None:

            raise HTTPException(
                status_code=400,
                detail="Driver not found",
            )

        if (
            self.plugin_manager
            .get_plugin(driver.driver_name)
            is None
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Plugin '{driver.driver_name}' "
                    "is not discovered"
                ),
            )

    async def _create_driver_configs(
        self,
        device: Device,
    ):

        if device.driver is None:
            return

        plugin = (
            self.plugin_manager
            .get_plugin(
                device.driver.driver_name
            )
        )

        if plugin is None:
            return

        for parameter in (
            plugin.info.config_parameters
        ):

            enum_info = ""

            if parameter.enum_values:

                enum_info = json.dumps(
                    parameter.enum_values
                )

            config = DeviceConfig(

                device_config_name=
                    parameter.name,

                data_side=
                    DataSide.AnySide,

                description=
                    parameter.description,

                value=
                    (
                        ""
                        if parameter.default is None
                        else str(
                            parameter.default
                        )
                    ),

                enum_info=enum_info,

                device_id=device.id,
            )

            self.repository.db.add(
                config
            )

        await self.repository.db.commit()

    async def _replace_driver_configs(
        self,
        device: Device,
    ):

        await self.repository.db.execute(

            delete(DeviceConfig)
            .where(
                DeviceConfig.device_id
                == device.id
            )
        )

        await self.repository.db.commit()

        device = await self.repository.get_by_id(
            device.id
        )

        await self._create_driver_configs(
            device
        )