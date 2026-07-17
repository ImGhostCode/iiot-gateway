from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate
from app.services.device_service import DeviceService
from app.db.models.device import Device

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


# from fastapi import APIRouter
# from fastapi import Depends

# from app.gateway.runtime import runtime

# router = APIRouter()


# @router.get("/{device_id}")

# async def get_runtime(device_id: int):

#     return runtime.polling.cache.get_device(
#         device_id
#     )