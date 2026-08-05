from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.system_config import SystemConfig
from app.db.session import get_db

from app.repositories.system_config_repository import SystemConfigRepository
from app.schemas.system_config_dto import SystemConfigCreate, SystemConfigUpdate, SystemConfigResponse
from app.services.system_config_service import SystemConfigService

router = APIRouter(tags=["System configs"])

def get_service(
    db: AsyncSession = Depends(get_db),
) -> SystemConfigService:
    return SystemConfigService(SystemConfigRepository(db))

@router.get("/", response_model=SystemConfigResponse)
async def get_config(
    service: SystemConfigService = Depends(get_service),
):
    return await service.get()

@router.put("/", response_model=SystemConfigResponse)
async def update_config(
    dto: SystemConfigUpdate,
    service: SystemConfigService = Depends(get_service),
):
    return await service.update(
        dto,
    )