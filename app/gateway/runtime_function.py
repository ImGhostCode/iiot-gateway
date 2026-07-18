from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.gateway.device_manager import DeviceManager
from app.gateway.polling_engine import PollingEngine
from app.gateway.event_bus import EventBus
from app.gateway.event import TagChangedEvent
from app.services.alarm_service import AlarmService
from app.services.history_service import HistoryService
from app.services.device_service import DeviceService
from app.repositories.device_repository import DeviceRepository
from app.services.mqtt_service import MQTTService
from app.services.ws_service import WebSocketService
from app.plugins.manager import PluginManager
from app.gateway.driver_factory import DriverFactory
from app.db.session import get_db
from app.core.logger import logger
from app.db.session import SessionLocal

bus = EventBus()
alarm = AlarmService()
history = HistoryService()
mqtt = MQTTService()
ws = WebSocketService()


bus.subscribe(TagChangedEvent, alarm.on_tag_changed)
bus.subscribe(TagChangedEvent, history.on_tag_changed)
bus.subscribe(TagChangedEvent, mqtt.on_tag_changed)
bus.subscribe(TagChangedEvent, ws.on_tag_changed)

plugin_manager = PluginManager()
driver_factory = DriverFactory(
    plugin_manager
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with SessionLocal() as session:
        device_service = DeviceService(DeviceRepository(db=session))
        device_manager = DeviceManager(bus,device_service)
        polling_engine = PollingEngine(device_manager)
        logger.info("Starting IoT Gateway...")

        plugin_manager.initialize()

        await device_manager.initialize()

        await polling_engine.start()

        logger.info("Gateway started.")

        yield

        logger.info("Stoping IoT Gateway...")

        await polling_engine.stop()

        await device_manager.shutdown()



