# GET    /api/v1/devices
# GET    /api/v1/devices/{id}
# POST   /api/v1/devices
# PUT    /api/v1/devices/{id}
# DELETE /api/v1/devices/{id}

# POST /api/v1/devices/{id}/connect
# POST /api/v1/devices/{id}/disconnect
# POST /api/v1/devices/{id}/restart

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.device_repository import DeviceRepository
from app.schemas.device_dto import DeviceCreate
from app.services.device_service import DeviceService
from app.db.models.device import Device
from app.gateway.device_manager import DeviceManager

router = APIRouter(tags=["Devices"])

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
