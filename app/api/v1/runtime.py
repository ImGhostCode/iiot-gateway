from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.gateway.device_manager import DeviceManager

router = APIRouter(tags=["Runtime"])

@router.get("/")
async def get(
    db: AsyncSession = Depends(get_db)
):
    return {"status: ok"}