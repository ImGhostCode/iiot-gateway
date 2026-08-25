from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_device_manager, require_operator
from app.db.session import get_db
from app.gateway.device_manager import DeviceManager
from app.repositories.device_repository import DeviceRepository
from app.repositories.device_variable_repository import DeviceVariableRepository
from app.schemas.device_variable_dto import (
    DeviceVariableCreate,
    DeviceVariableResponse,
    DeviceVariableRuntimeResponse,
    DeviceVariableUpdate,
    DeviceVariableWriteRequest,
    DeviceVariableWriteResponse,
)
from app.services.device_variable_service import DeviceVariableService
from app.db.models.base import ProtectTypeEnum

router = APIRouter(tags=["Device Variables"])


def get_service(db: AsyncSession = Depends(get_db)) -> DeviceVariableService:
    return DeviceVariableService(
        DeviceVariableRepository(db),
        DeviceRepository(db),
    )



async def _restart_device_runtime(
    device_id: UUID,
    manager: DeviceManager,
    db: AsyncSession,
):
    """
    Reload the device from database before rebuilding runtime.

    Important:
    Never restart using the old SQLAlchemy Device object because
    its device_variables relationship may be stale after create/delete.
    """

    runtime = manager.get(device_id)

    if runtime is None:
        return

    device_repository = DeviceRepository(db)

    fresh_device = await device_repository.get_by_id(
        device_id
    )

    if fresh_device is None:
        return

    await manager.restart(
        fresh_device
    )

def merge_runtime_state(
    variable,
    manager: DeviceManager,
):
    runtime = manager.get(variable.device_id)

    if runtime is None:
        return variable

    runtime_variable = runtime.variables.get(
        str(variable.id)
    )

    if runtime_variable is None:
        return variable

    variable.value = runtime_variable.value

    variable.cooked_value = (
        runtime_variable.cooked_value
    )

    variable.message = (
        runtime_variable.message
    )

    variable.quality = (
        runtime_variable.quality
    )

    variable.timestamp = (
        runtime_variable.timestamp
    )

    return variable

@router.get("/", response_model=list[DeviceVariableResponse])
async def get_variables(
    service: DeviceVariableService = Depends(get_service),
    manager: DeviceManager = Depends(get_device_manager),
    user=Depends(get_current_user),
):
    variables = await service.get_all()

    for variable in variables:
        merge_runtime_state(
            variable,
            manager,
        )

    return variables


@router.get("/{device_id}", response_model=list[DeviceVariableResponse])
async def get_device_variables(
    device_id: UUID,
    service: DeviceVariableService = Depends(get_service),
    manager: DeviceManager = Depends(get_device_manager),
    user=Depends(get_current_user),
):
    variables = await service.get_by_device(
        device_id
    )

    for variable in variables:
        merge_runtime_state(
            variable,
            manager,
        )

    return variables


@router.get("/{device_id}/{variable_id}", response_model=DeviceVariableResponse)
async def get_device_variable(
    device_id: UUID,
    variable_id: UUID,
    service: DeviceVariableService = Depends(get_service),
    manager: DeviceManager = Depends(get_device_manager),
    user=Depends(get_current_user),
):
    variable = await service.get_by_id(
        device_id,
        variable_id,
    )

    if variable is None:
        raise HTTPException(
            status_code=404,
            detail="Device variable not found",
        )

    merge_runtime_state(
        variable,
        manager,
    )

    return variable


@router.post(
    "/{device_id}",
    response_model=DeviceVariableResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_device_variable(
    device_id: UUID,
    dto: DeviceVariableCreate,
    service: DeviceVariableService = Depends(get_service),
    manager: DeviceManager = Depends(get_device_manager),
    db: AsyncSession = Depends(get_db),
    user=Depends(require_operator),
):

    variable = await service.create(
        device_id,
        dto,
    )

    # Important:
    # Rebuild runtime so the newly created variable
    # becomes immediately readable/writable.
    await _restart_device_runtime(
        device_id,
        manager,
        db,
    )

    return variable


@router.put(
    "/{device_id}/{variable_id}",
    response_model=DeviceVariableResponse,
)
async def update_device_variable(
    device_id: UUID,
    variable_id: UUID,
    dto: DeviceVariableUpdate,
    service: DeviceVariableService = Depends(get_service),
    manager: DeviceManager = Depends(get_device_manager),
    db: AsyncSession = Depends(get_db),
    user=Depends(require_operator),
):
    variable = await service.update(device_id, variable_id, dto)
    if variable is None:
        raise HTTPException(status_code=404, detail="Device variable not found")

    await _restart_device_runtime(
        device_id,
        manager,
        db,
    )

    return variable


@router.delete(
    "/{device_id}/{variable_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_device_variable(
    device_id: UUID,
    variable_id: UUID,
    service: DeviceVariableService = Depends(get_service),
    manager: DeviceManager = Depends(get_device_manager),
    db: AsyncSession = Depends(get_db),
    user=Depends(require_operator),
):
    deleted = await service.delete(device_id, variable_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device variable not found")

    # Reload device AFTER deletion.
    #
    # This guarantees RuntimeBuilder sees the current
    # device_variables collection.
    await _restart_device_runtime(
        device_id,
        manager,
        db,
    )

@router.get(
    "/{device_id}/{variable_id}/runtime",
    response_model=DeviceVariableRuntimeResponse,
)
async def get_runtime_variable(
    device_id: UUID,
    variable_id: UUID,
    manager: DeviceManager = Depends(get_device_manager),
    user=Depends(get_current_user),
):
    runtime = manager.get(device_id)
    if runtime is None:
        raise HTTPException(status_code=404, detail="Device is not running")

    variable = runtime.variables.get(str(variable_id))
    if variable is None:
        raise HTTPException(status_code=404, detail="Runtime variable not found")

    return DeviceVariableRuntimeResponse(
        id=UUID(variable.id),
        device_id=device_id,
        name=variable.name,
        value=variable.value,
        cooked_value=variable.cooked_value,
        message=variable.message,
        quality=variable.quality,
        timestamp=variable.timestamp,
    )


@router.post(
    "/{device_id}/{variable_id}/write",
    response_model=DeviceVariableWriteResponse,
)
async def write_device_variable(
    device_id: UUID,
    variable_id: UUID,
    dto: DeviceVariableWriteRequest,
    manager: DeviceManager = Depends(get_device_manager),
    user=Depends(require_operator),
):
    runtime = manager.get(device_id)
    if runtime is None:
        raise HTTPException(status_code=409, detail="Device is not running")

    # IMPORTANT:
    # Resolve the variable ONLY from the current runtime.
    #
    # This prevents an old/deleted variable from being
    # accessed through the write API.
    runtime_variable = runtime.variables.get(
        str(variable_id)
    )

    if runtime_variable is None:
        raise HTTPException(
            status_code=404,
            detail="Device variable not found",
        )

    variable = next(
        (
            v
            for v in runtime.device.device_variables
            if v.id == variable_id
        ),
        None,
    )

    if variable is None:
        raise HTTPException(
            status_code=404,
            detail="Device variable not found",
        )

    if (
        variable.protect_type
        == ProtectTypeEnum.ReadOnly
    ):
        raise HTTPException(
            status_code=403,
            detail="Variable is read-only",
        )

    try:

        await runtime.driver.write(
            variable,
            dto.value,
        )

    except NotImplementedError:

        raise HTTPException(
            status_code=501,
            detail=(
                f"Driver '{runtime.device.driver.driver_name}' "
                "does not support variable writes"
            ),
        )

    except Exception as ex:

        variable.message = str(ex)

        raise HTTPException(
            status_code=502,
            detail=f"Variable write failed: {ex}",
        )

    return DeviceVariableWriteResponse(
        id=variable_id,
        device_id=device_id,
        name=variable.name,
        requested_value=dto.value,
        success=True,
        message="Variable write completed",
    )