from app.gateway.driver_factory import DriverFactory
from app.plugins.base_driver import BaseDriver

class DeviceManager:

    def __init__(self):
        self.devices : dict[int, BaseDriver] = {}

    async def initialize(self):
        print("Loading devices from database...")
        #
        # Later:
        #
        # devices = await repository.get_all()
        #

    async def add(self, device):
        driver = DriverFactory.create(device)
        await driver.connect()
        self.devices[device.id] = driver

    async def remove(self, device_id):
        driver = self.devices.get(device_id)
        if driver:
            await driver.disconnect()
            del self.devices[device_id]

    def get(self, device_id):
        return self.devices.get(device_id)

    async def shutdown(self):
        for driver in self.devices.values():
            await driver.disconnect()
        self.devices.clear()