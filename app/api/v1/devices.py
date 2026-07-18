from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate
from app.services.device_service import DeviceService
from app.db.models.device import Device
from app.gateway.device_manager import DeviceManager

router = APIRouter()

@router.get("/")
async def get_devices(
    db: AsyncSession = Depends(get_db)
):
    service = DeviceService(DeviceRepository(db))
    return await service.get_all()

@router.post("/")
async def create_device(
    dto: DeviceCreate,
    db: AsyncSession = Depends(get_db)
):
    service = DeviceService(DeviceRepository(db))
    device = Device(**dto.model_dump())
    return await service.create(device)


@router.get("/runtime")
async def runtime_status(manager: DeviceManager):
    return [
        {
            "id": runtime.device.id,
            "name": runtime.device.device_name,
            "connected": runtime.connected,
            "reads": runtime.statistics.read_count,
            "errors": runtime.statistics.error_count,
            "last_poll": runtime.statistics.last_poll,
        }
        for runtime in manager.devices.values()
    ]

# @router.get("/{device_id}")

# async def get_runtime(device_id: int):

#     return runtime.polling.cache.get_device(
#         device_id
#     )