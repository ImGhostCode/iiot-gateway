from uuid import UUID

from fastapi import (
    HTTPException,
    status,
)

from app.db.models.driver import Driver
from app.repositories.plugin_repository import (
    PluginRepository,
)

from app.schemas.driver_dto import (
    DriverCreate,
    DriverUpdate,
)

from app.plugins.manager import PluginManager


class PluginService:

    def __init__(
        self,
        repository: PluginRepository,
        plugin_manager: PluginManager,
    ):

        self.repository = repository

        self.plugin_manager = (
            plugin_manager
        )

    async def get_all(self):

        return await self.repository.get_all()

    async def get_by_id(
        self,
        driver_id: UUID,
    ):

        return await self.repository.get_by_id(
            driver_id
        )

    def get_discovered(self):

        return self.plugin_manager.all()

    def get_discovered_by_name(
        self,
        name: str,
    ):

        plugin = (
            self.plugin_manager
            .get_plugin(name)
        )

        if plugin is None:

            raise HTTPException(
                status_code=404,
                detail="Plugin not found",
            )

        return plugin

    def get_config_schema(
        self,
        name: str,
    ):

        plugin = (
            self.get_discovered_by_name(name)
        )

        return plugin.info.config_parameters

    async def get_available(self):

        registered = (
            await self.repository.get_all()
        )

        registered_by_file = {

            item.file_name.lower():
                item

            for item in registered
        }

        result = []

        for plugin in (
            self.plugin_manager.all()
        ):

            existing = (
                registered_by_file.get(
                    plugin.info.name.lower()
                )
            )

            result.append(

                {
                    "name":
                        plugin.info.name,

                    "version":
                        plugin.info.version,

                    "author":
                        plugin.info.author,

                    "description":
                        plugin.info.description,

                    "driver":
                        f"{plugin.driver.__module__}."
                        f"{plugin.driver.__name__}",

                    "config_parameters":
                        plugin.info.config_parameters,

                    "registered":
                        existing is not None,

                    "driver_id":
                        existing.id
                        if existing
                        else None,
                }
            )

        return result

    async def create(
        self,
        dto: DriverCreate,
    ):

        plugin = (
            self.plugin_manager
            .get_plugin(dto.file_name)
        )

        if plugin is None:

            raise HTTPException(

                status_code=
                    status.HTTP_400_BAD_REQUEST,

                detail=
                    f"Plugin '{dto.file_name}' "
                    "is not discovered",
            )

        existing = (
            await self.repository
            .get_by_file_name(
                plugin.info.name
            )
        )

        if existing is not None:

            raise HTTPException(

                status_code=
                    status.HTTP_409_CONFLICT,

                detail=
                    "Plugin is already registered",
            )

        driver = Driver(

            driver_name=
                plugin.info.name,

            file_name=
                plugin.info.name,

            assemble_name=
                f"{plugin.driver.__module__}."
                f"{plugin.driver.__name__}",

            authorizes_num=
                dto.authorizes_num,
        )

        return await self.repository.create(
            driver
        )

    async def update(
        self,
        driver_id: UUID,
        dto: DriverUpdate,
    ):

        driver = (
            await self.repository
            .get_by_id(driver_id)
        )

        if driver is None:
            return None

        if dto.file_name is not None:

            plugin = (
                self.plugin_manager
                .get_plugin(
                    dto.file_name
                )
            )

            if plugin is None:

                raise HTTPException(

                    status_code=400,

                    detail=
                        f"Plugin "
                        f"'{dto.file_name}' "
                        "is not discovered",
                )

            existing = (
                await self.repository
                .get_by_file_name(
                    plugin.info.name
                )
            )

            if (
                existing is not None
                and existing.id != driver.id
            ):

                raise HTTPException(

                    status_code=409,

                    detail=
                        "Plugin is already "
                        "registered",
                )

            driver.driver_name = (
                plugin.info.name
            )

            driver.file_name = (
                plugin.info.name
            )

            driver.assemble_name = (

                f"{plugin.driver.__module__}."
                f"{plugin.driver.__name__}"
            )

        if dto.authorizes_num is not None:

            driver.authorizes_num = (
                dto.authorizes_num
            )

        return await self.repository.update(
            driver
        )

    async def delete(
        self,
        driver_id: UUID,
    ) -> bool:

        driver = (
            await self.repository
            .get_by_id(driver_id)
        )

        if driver is None:
            return False

        await self.repository.delete(
            driver
        )

        return True