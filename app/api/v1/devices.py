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
    get_device_manager,
    require_admin,
    require_operator,
)

from app.db.session import get_db

from app.gateway.device_manager import (
    DeviceManager,
)

from app.plugins.manager import (
    PluginManager,
)

from app.repositories.device_repository import (
    DeviceRepository,
)

from app.repositories.plugin_repository import (
    PluginRepository,
)

from app.schemas.device_dto import (
    DeviceCreate,
    DeviceResponse,
    DeviceRuntimeStatusResponse,
    DeviceUpdate,
    DeviceVariableRuntimeResponse,
)

from app.services.device_service import (
    DeviceService,
)


router = APIRouter(
    tags=["Devices"]
)


def get_plugin_manager(
) -> PluginManager:

    from app.gateway.runtime_function import (
        plugin_manager,
    )

    return plugin_manager


def get_service(
    db: AsyncSession = Depends(get_db),
    plugin_manager: PluginManager = Depends(
        get_plugin_manager
    ),
) -> DeviceService:

    return DeviceService(

        repository=
            DeviceRepository(db),

        plugin_repository=
            PluginRepository(db),

        plugin_manager=
            plugin_manager,
    )


# =========================================================
# CRUD
# =========================================================

@router.get(
    "/",
    response_model=list[DeviceResponse],
)
async def get_devices(
    service: DeviceService = Depends(
        get_service
    ),
):

    return await service.get_all()


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
async def get_device(
    device_id: UUID,

    service: DeviceService = Depends(
        get_service
    ),
):

    device = await service.get_by_id(
        device_id
    )

    if device is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return device


@router.post(
    "/",

    response_model=DeviceResponse,

    status_code=status.HTTP_201_CREATED,

    dependencies=[
        Depends(require_admin)
    ],
)
async def create_device(
    dto: DeviceCreate,

    service: DeviceService = Depends(
        get_service
    ),

):

    return await service.create(
        dto
    )


@router.put(
    "/{device_id}",

    response_model=DeviceResponse,

    dependencies=[
        Depends(require_admin)
    ],
)
async def update_device(
    device_id: UUID,

    dto: DeviceUpdate,

    service: DeviceService = Depends(
        get_service
    ),

    manager: DeviceManager = Depends(
        get_device_manager
    ),
):

    device = await service.get_by_id(
        device_id
    )

    if device is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    was_running = (
        manager.get(device_id)
        is not None
    )

    if was_running:

        await manager.remove(
            device_id
        )

    updated = await service.update(
        device_id,
        dto,
    )

    if updated is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    if (
        updated.device_type_enum.name
        == "Device"
        and updated.auto_start
        and was_running
    ):

        await manager.start(
            updated
        )

    return updated


@router.delete(
    "/{device_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    dependencies=[
        Depends(require_admin)
    ],
)
async def delete_device(
    device_id: UUID,

    service: DeviceService = Depends(
        get_service
    ),

    manager: DeviceManager = Depends(
        get_device_manager
    ),
):

    device = await service.get_by_id(
        device_id
    )

    if device is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    await manager.remove(
        device_id
    )

    deleted = await service.delete(
        device_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )


# =========================================================
# Runtime control
# =========================================================

@router.post(
    "/{device_id}/start",

    response_model=DeviceRuntimeStatusResponse,

    dependencies=[
        Depends(require_operator)
    ],
)
async def start_device(
    device_id: UUID,

    service: DeviceService = Depends(
        get_service
    ),

    manager: DeviceManager = Depends(
        get_device_manager
    ),
):

    device = await service.get_by_id(
        device_id
    )

    if device is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    if (
        device.device_type_enum.name
        != "Device"
    ):

        raise HTTPException(
            status_code=400,
            detail="Groups cannot be started",
        )

    runtime = await manager.start(
        device
    )

    return _runtime_status(
        runtime
    )


@router.post(
    "/{device_id}/stop",

    status_code=status.HTTP_204_NO_CONTENT,

    dependencies=[
        Depends(require_operator)
    ],
)
async def stop_device(
    device_id: UUID,

    manager: DeviceManager = Depends(
        get_device_manager
    ),
):

    stopped = await manager.stop(
        device_id
    )

    if not stopped:

        raise HTTPException(
            status_code=404,
            detail="Device is not running",
        )


@router.post(
    "/{device_id}/restart",

    response_model=DeviceRuntimeStatusResponse,

    dependencies=[
        Depends(require_operator)
    ],
)
async def restart_device(
    device_id: UUID,

    service: DeviceService = Depends(
        get_service
    ),

    manager: DeviceManager = Depends(
        get_device_manager
    ),
):

    device = await service.get_by_id(
        device_id
    )

    if device is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    if (
        device.device_type_enum.name
        != "Device"
    ):

        raise HTTPException(
            status_code=400,
            detail="Groups cannot be restarted",
        )

    runtime = await manager.restart(
        device
    )

    return _runtime_status(
        runtime
    )


# =========================================================
# Runtime status
# =========================================================

@router.get(
    "/{device_id}/status",

    response_model=DeviceRuntimeStatusResponse,
)
async def get_device_status(
    device_id: UUID,

    service: DeviceService = Depends(
        get_service
    ),

    manager: DeviceManager = Depends(
        get_device_manager
    ),
):

    device = await service.get_by_id(
        device_id
    )

    if device is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    runtime = manager.get(
        device_id
    )

    if runtime is None:

        return DeviceRuntimeStatusResponse(

            id=device.id,

            device_name=
                device.device_name,

            connected=False,

            polling=False,

            read_count=0,

            error_count=0,

            reconnect_count=0,

            last_poll=None,

            last_error=None,
        )

    return _runtime_status(
        runtime
    )


# =========================================================
# Runtime variables
# =========================================================

@router.get(
    "/{device_id}/variables/runtime",

    response_model=list[
        DeviceVariableRuntimeResponse
    ],
)
async def get_runtime_variables(
    device_id: UUID,

    service: DeviceService = Depends(
        get_service
    ),

    manager: DeviceManager = Depends(
        get_device_manager
    ),
):

    device = await service.get_by_id(
        device_id
    )

    if device is None:

        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    runtime = manager.get(
        device_id
    )

    if runtime is None:
        return []

    result = []

    for variable in (
        runtime.variables.values()
    ):

        result.append(

            DeviceVariableRuntimeResponse(

                id=UUID(variable.id),

                name=variable.name,

                value=variable.value,

                quality=variable.quality,

                timestamp=variable.timestamp,
            )
        )

    return result


def _runtime_status(
    runtime,
) -> DeviceRuntimeStatusResponse:

    stats = runtime.statistics

    return DeviceRuntimeStatusResponse(

        id=runtime.device.id,

        device_name=
            runtime.device.device_name,

        connected=
            runtime.connected,

        polling=
            runtime.polling,

        read_count=
            stats.read_count,

        error_count=
            stats.error_count,

        reconnect_count=
            stats.reconnect_count,

        last_poll=
            stats.last_poll,

        last_error=
            stats.last_error,
    )