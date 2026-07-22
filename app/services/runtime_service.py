from app.db.models.driver import Driver
from app.repositories.runtime_repository import RuntimRepository

class RuntimeService:
    def __init__(self, repository: RuntimRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()
    
    async def create(self, driver: Driver):
        return await self.repository.add(driver)