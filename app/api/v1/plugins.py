from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.dependencies import (
    require_admin,
)

from app.db.session import get_db

from app.plugins.manager import (
    PluginManager,
)

from app.repositories.plugin_repository import (
    PluginRepository,
)

from app.schemas.driver_dto import (
    DiscoveredPluginResponse,
    DriverCreate,
    DriverResponse,
    DriverUpdate,
    PluginAvailableResponse,
    PluginConfigParameterResponse,
)

from app.services.plugin_service import (
    PluginService,
)


router = APIRouter(
    tags=["Plugins"]
)


def get_plugin_manager() -> PluginManager:

    from app.gateway.runtime_function import (
        plugin_manager,
    )

    return plugin_manager


def get_service(
    db: AsyncSession = Depends(get_db),

    plugin_manager: PluginManager = Depends(
        get_plugin_manager
    ),
) -> PluginService:

    return PluginService(
        PluginRepository(db),
        plugin_manager,
    )


# ---------------------------------------------------------
# Runtime discovered plugins
# ---------------------------------------------------------

@router.get(
    "/discovered",
    response_model=list[
        DiscoveredPluginResponse
    ],
)
async def get_discovered_plugins(
    service: PluginService = Depends(
        get_service
    ),
):

    result = []

    for plugin in (
        service.get_discovered()
    ):

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
            }
        )

    return result


@router.get(
    "/discovered/{plugin_name}",
    response_model=DiscoveredPluginResponse,
)
async def get_discovered_plugin(
    plugin_name: str,

    service: PluginService = Depends(
        get_service
    ),
):

    plugin = (
        service.get_discovered_by_name(
            plugin_name
        )
    )

    return {

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
    }


@router.get(
    "/discovered/{plugin_name}/config-schema",

    response_model=list[
        PluginConfigParameterResponse
    ],
)
async def get_plugin_config_schema(
    plugin_name: str,

    service: PluginService = Depends(
        get_service
    ),
):

    return service.get_config_schema(
        plugin_name
    )


# ---------------------------------------------------------
# Available plugins
# ---------------------------------------------------------

@router.get(
    "/available",
    response_model=list[
        PluginAvailableResponse
    ],
)
async def get_available_plugins(
    service: PluginService = Depends(
        get_service
    ),
):

    return await service.get_available()


# ---------------------------------------------------------
# Registered plugins / drivers
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=list[DriverResponse],
)
async def get_plugins(
    service: PluginService = Depends(
        get_service
    ),
):

    return await service.get_all()


@router.get(
    "/{plugin_id}",
    response_model=DriverResponse,
)
async def get_plugin(
    plugin_id: UUID,

    service: PluginService = Depends(
        get_service
    ),
):

    driver = await service.get_by_id(
        plugin_id
    )

    if driver is None:

        raise HTTPException(
            status_code=404,
            detail="Plugin not found",
        )

    return driver


@router.post(
    "/",

    response_model=DriverResponse,

    status_code=status.HTTP_201_CREATED,

    dependencies=[
        Depends(require_admin)
    ],
)
async def create_plugin(
    dto: DriverCreate,

    service: PluginService = Depends(
        get_service
    ),
):

    return await service.create(dto)


@router.put(
    "/{plugin_id}",

    response_model=DriverResponse,

    dependencies=[
        Depends(require_admin)
    ],
)
async def update_plugin(
    plugin_id: UUID,

    dto: DriverUpdate,

    service: PluginService = Depends(
        get_service
    ),
):

    driver = await service.update(
        plugin_id,
        dto,
    )

    if driver is None:

        raise HTTPException(
            status_code=404,
            detail="Plugin not found",
        )

    return driver


@router.delete(
    "/{plugin_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    dependencies=[
        Depends(require_admin)
    ],
)
async def delete_plugin(
    plugin_id: UUID,

    service: PluginService = Depends(
        get_service
    ),
):

    deleted = await service.delete(
        plugin_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Plugin not found",
        )