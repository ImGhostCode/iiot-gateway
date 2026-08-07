from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.driver import Driver
from app.repositories.repository import Repository


class PluginRepository(
    Repository[Driver]
):

    def __init__(
        self,
        db: AsyncSession,
    ):

        super().__init__(
            db,
            Driver,
        )

    async def get_by_id(
        self,
        driver_id,
    ):

        return await self.db.get(
            Driver,
            driver_id,
        )

    async def get_by_file_name(
        self,
        file_name: str,
    ):

        result = await self.db.execute(

            select(Driver)
            .where(
                Driver.file_name == file_name
            )

        )

        return result.scalar_one_or_none()

    async def get_by_driver_name(
        self,
        driver_name: str,
    ):

        result = await self.db.execute(

            select(Driver)
            .where(
                Driver.driver_name
                == driver_name
            )

        )

        return result.scalar_one_or_none()