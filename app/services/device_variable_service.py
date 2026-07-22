from app.db.models.device_variable import DeviceVariable
from app.repositories.device_variable_repository import DeviceVariableRepository

class DeviceVariableService:
    def __init__(self, repository: DeviceVariableRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()
    
    async def create(self, variable: DeviceVariable):
        return await self.repository.add(variable)