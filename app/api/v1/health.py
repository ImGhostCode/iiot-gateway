from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter(tags=["Health"])

@router.get("/")
async def get(
    db: AsyncSession = Depends(get_db)
):
    return {"status: ok"}