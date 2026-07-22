from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.plugin_service import PluginService
from app.repositories.plugin_repository import PluginRepository
from app.db.models.driver import Driver
from app.schemas.driver_dto import DriverCreate
from app.db.session import get_db

router = APIRouter(tags=["Plugins"])

@router.get("/")
async def get_plugins(
    db: AsyncSession = Depends(get_db)
):
    service = PluginService(PluginRepository(db))
    return await service.get_all()

@router.post("/")
async def create_plugin(
    dto: DriverCreate,
    db: AsyncSession = Depends(get_db)
):
    service = PluginService(PluginRepository(db))
    driver = Driver(**dto.model_dump())
    return await service.create(driver)
