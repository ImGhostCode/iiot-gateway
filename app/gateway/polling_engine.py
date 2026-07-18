import asyncio

from app.gateway.device_manager import DeviceManager
from app.gateway.runtime_cache import RuntimeCache
from app.gateway.tag_processor import TagProcessor
from app.gateway.event_bus import EventBus
from app.gateway.event import TagChangedEvent
from app.services.alarm_service import AlarmService
from app.services.history_service import HistoryService
from app.services.mqtt_service import MQTTService
from app.services.ws_service import WebSocketService

class PollingEngine:
    def __init__(self, manager : DeviceManager) -> None:
        self.manager = manager
        # self.cache = RuntimeCache()
        self.running = False
        # self.task = None
        # bus = EventBus()
        # alarm = AlarmService()
        # history = HistoryService()
        # mqtt = MQTTService()
        # ws = WebSocketService()

        # bus.subscribe(TagChangedEvent, alarm.on_tag_changed)
        # bus.subscribe(TagChangedEvent, history.on_tag_changed)
        # bus.subscribe(TagChangedEvent, mqtt.on_tag_changed)
        # bus.subscribe(TagChangedEvent, ws.on_tag_changed)
        # self.processor = TagProcessor(bus)
    
    async def start(self):
        self.running = True
        self.task = asyncio.create_task(self.run())

    async def stop(self):
        self.running = False
        if self.task:
            self.task.cancel()

    # async def run(self):
    #     while self.running:
    #         for driver in self.manager.devices.values():
    #             try:
    #                 await driver.read()
    #             except Exception as ex:
    #                 print(ex)
    #         await asyncio.sleep(1)

    async def run(self):
        for runtime in self.manager.devices.values():
            await self.manager.add(runtime.device)
        # while self.running:
        #     tasks = []
        #     for runtime in self.manager.devices.values():
        #         tasks.append(
        #             asyncio.create_task(runtime.driver.read())
        #         )
        #     if tasks:
        #         await asyncio.gather(*tasks, return_exceptions=True)
        #     await asyncio.sleep(1)

    # async def run(self):
    #     while True:
    #         for device_id, driver in self.manager.drivers.values():
    #             try:
    #                 variables = await driver.read()
    #                 self.cache.update(device_id, variables)
    #             except Exception as ex:
    #                 print(ex)
    #         await asyncio.sleep(1)

    # async def polling_device(self, runtime):
    #     values = await runtime.driver.read()
    #     await self.processor.process(runtime, values)

    # async def device_loop(self, runtime):
    #     while runtime.connected:
    #         values = await runtime.driver.read()
    #         await self.processor.process(runtime, values)
    #         await asyncio.sleep(runtime.device.enforce_period / 1000)
