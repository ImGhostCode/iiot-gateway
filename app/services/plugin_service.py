from app.db.models.driver import Driver
from app.repositories.plugin_repository import PluginRepository

class PluginService:
    def __init__(self, repository: PluginRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()
    
    async def create(self, driver: Driver):
        return await self.repository.add(driver)