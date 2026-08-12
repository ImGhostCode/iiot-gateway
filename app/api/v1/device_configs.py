from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import (
    get_current_user,
    require_operator,
)

from app.db.session import get_db

from app.repositories.device_config_repository import (
    DeviceConfigRepository,
)

from app.repositories.device_repository import (
    DeviceRepository,
)

from app.schemas.device_config_dto import (
    DeviceConfigCreate,
    DeviceConfigResponse,
    DeviceConfigSchemaItem,
    DeviceConfigSchemaResponse,
    DeviceConfigUpdate,
)

from app.services.device_config_service import (
    DeviceConfigService,
)

from app.gateway.device_manager import DeviceManager
from app.core.dependencies import get_device_manager


router = APIRouter(
    tags=["Device Configs"]
)


def get_service(
    db: AsyncSession = Depends(get_db),
):

    return DeviceConfigService(
        DeviceConfigRepository(db)
    )


@router.get(
    "/{device_id}/configs",
    response_model=list[DeviceConfigResponse],
)
async def get_device_configs(
    device_id: str,
    service: DeviceConfigService = Depends(
        get_service
    ),
    user=Depends(get_current_user),
):

    return await service.get_by_device(
        device_id
    )


@router.get(
    "/{device_id}/configs/{config_id}",
    response_model=DeviceConfigResponse,
)
async def get_device_config(
    device_id: str,
    config_id: str,
    service: DeviceConfigService = Depends(
        get_service
    ),
    user=Depends(get_current_user),
):

    config = await service.get_by_id(
        device_id,
        config_id,
    )

    if config is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device config not found",
        )

    return config


@router.post(
    "/{device_id}/configs",
    response_model=DeviceConfigResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_device_config(
    device_id: str,
    dto: DeviceConfigCreate,
    service: DeviceConfigService = Depends(
        get_service
    ),
    user=Depends(require_operator),
):

    return await service.create(
        device_id,
        dto,
    )


@router.put(
    "/{device_id}/configs/{config_id}",
    response_model=DeviceConfigResponse,
)
async def update_device_config(
    device_id: str,
    config_id: str,
    dto: DeviceConfigUpdate,
    service: DeviceConfigService = Depends(
        get_service
    ),
    manager: DeviceManager = Depends(
        get_device_manager
    ),
    user=Depends(require_operator),
):

    config = await service.update(
        device_id,
        config_id,
        dto,
    )

    if config is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device config not found",
        )

    await _reload_device(
        device_id,
        manager,
    )

    return config


@router.delete(
    "/{device_id}/configs/{config_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_device_config(
    device_id: str,
    config_id: str,
    service: DeviceConfigService = Depends(
        get_service
    ),
    manager: DeviceManager = Depends(
        get_device_manager
    ),
    user=Depends(require_operator),
):

    deleted = await service.delete(
        device_id,
        config_id,
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device config not found",
        )

    await _reload_device(
        device_id,
        manager,
    )


async def _reload_device(
    device_id,
    manager: DeviceManager,
):

    runtime = manager.get(device_id)

    if runtime is None:

        return

    driver = runtime.driver

    await driver.disconnect()

    await driver.initialize()

    await driver.connect()

    runtime.connected = driver.connected

@router.get(
    "/{device_id}/config-schema",
    response_model=DeviceConfigSchemaResponse,
)
async def get_device_config_schema(
    device_id: str,
    db: AsyncSession = Depends(get_db),
    request: Request = None,
    user=Depends(get_current_user),
):

    device_repository = DeviceRepository(db)

    device = await device_repository.get_by_id(
        device_id
    )

    if device is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    if device.driver is None:

        return DeviceConfigSchemaResponse(
            device_id=device.id,
            driver=None,
            configs=[],
        )

    plugin_manager = request.app.state.plugin_manager

    driver_cls = plugin_manager.get_driver(
        device.driver.driver_name
    )

    configs = []

    for item in driver_cls.config_schema():

        configs.append(
            DeviceConfigSchemaItem(

                name=item.name,

                description=item.description,

                default=item.default,

                data_side=item.data_side,

                enum_info=item.enum_info,

            )
        )

    return DeviceConfigSchemaResponse(

        device_id=device.id,

        driver=device.driver.driver_name,

        configs=configs,

    )