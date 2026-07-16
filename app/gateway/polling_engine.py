import asyncio

from app.gateway.device_manager import DeviceManager

class PollingEngine:
    def __init__(self, manager : DeviceManager) -> None:
        self.manager = manager
        self.running = False
        self.task = None
    
    async def start(self):
        self.running = True
        self.task = asyncio.create_task(self.run())

    async def stop(self):
        self.running = False
        if self.task:
            self.task.cancel()

    async def run(self):
        while self.running:
            for driver in self.manager.devices.values():
                try:
                    await driver.read()
                except Exception as ex:
                    print(ex)
            await asyncio.sleep(1)