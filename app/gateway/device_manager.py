from app.gateway.driver_factory import DriverFactory
from app.plugins.base_driver import BaseDriver
from app.gateway.runtime.runtime_device import RuntimeDevice
from app.gateway.runtime.runtime_builder import RuntimeBuilder

class DeviceManager:

    def __init__(self):
        # self.devices : dict[int, BaseDriver] = {}
        # self.drivers = {}
        self.devices: dict[int, RuntimeDevice] = {}

    # async def load(self, devices):
    #     for device in devices:
    #         driver = await DriverFactory.create(device)
    #         await driver.connect()
    #         self.drivers[device.id] = driver

    # async def initialize(self):
    #     print("Loading devices from database...")
    #     #
    #     # Later:
    #     #
    #     # devices = await repository.get_all()
    #     #

    # async def add(self, device):
    #     driver = DriverFactory.create(device)
    #     await driver.connect()
    #     self.devices[device.id] = driver

    # async def remove(self, device_id):
    #     driver = self.devices.get(device_id)
    #     if driver:
    #         await driver.disconnect()
    #         del self.devices[device_id]

    # def get(self, device_id):
    #     return self.devices.get(device_id)

    # async def shutdown(self):
    #     for driver in self.devices.values():
    #         await driver.disconnect()
    #     self.devices.clear()

    async def add(self, device):
        driver = await DriverFactory.create(device)
        runtime = RuntimeBuilder.build(device, driver)
        await driver.connect()
        runtime.connected = True
        self.devices[device.id] = runtime

    def get(self, id):
        return self.devices.get(id)
    
    async def remove(self, device_id):
        runtime = self.devices.pop(
            device_id,
            None,
        )
        if runtime:
            await runtime.driver.disconnect()