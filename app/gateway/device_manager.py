import asyncio

from app.core.logger import logger

from app.gateway.driver_factory import DriverFactory
from app.plugins.base_driver import BaseDriver
from app.gateway.runtime.runtime_device import RuntimeDevice
from app.gateway.runtime.runtime_builder import RuntimeBuilder
from app.gateway.device_worker import DeviceWorker
from app.services.device_service import DeviceService

class DeviceManager:

    def __init__(self, bus , device_service : DeviceService):
        self.bus = bus
        self.device_service = device_service
        # self.devices : dict[int, BaseDriver] = {}
        # self.drivers = {}
        self.devices: dict[int, RuntimeDevice] = {}

    # async def load(self, devices):
    #     for device in devices:
    #         driver = await DriverFactory.create(device)
    #         await driver.connect()
    #         self.drivers[device.id] = driver

    async def initialize(self):
        logger.info("Loading devices from database...")
        devices = await self.device_service.get_all()
        for device in devices:
            await self.add(device)
        logger.info(
            f"Initialized {len(self.devices)} devices"
        )

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

    async def shutdown(self):
        for runtime in self.devices.values():
            if runtime.polling_task:
                runtime.polling_task.cancel()
            await runtime.driver.disconnect()
        self.devices.clear()

    async def add(self, device):
        from app.gateway.runtime_function import driver_factory
        driver = await driver_factory.create(device)
        runtime = RuntimeBuilder.build(device, driver)
        await driver.connect()
        runtime.connected = True
        worker = DeviceWorker(runtime, self.bus)
        runtime.polling_task = asyncio.create_task(worker.start())
        self.devices[device.id] = runtime

    def get(self, id):
        return self.devices.get(id)
    
    async def remove(self, device_id):
        runtime = self.devices.pop(
            device_id,
            None,
        )
        if runtime is None:
            return
        if runtime.polling_task:
            runtime.polling_task.cancel()
        await runtime.driver.disconnect()