from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.gateway.device_manager import (
    DeviceManager,
)

from app.gateway.polling_engine import (
    PollingEngine,
)

from app.gateway.event_bus import (
    EventBus,
)

from app.gateway.event import (
    TagChangedEvent,
)

from app.services.alarm_service import (
    AlarmService,
)

from app.services.history_service import (
    HistoryService,
)

from app.services.mqtt_service import (
    MQTTService,
)

from app.services.ws_service import (
    WebSocketService,
)

from app.plugins.manager import (
    PluginManager,
)

from app.gateway.driver_factory import (
    DriverFactory,
)

from app.db.session import (
    SessionLocal,
)

from app.repositories.device_repository import (
    DeviceRepository,
)

from app.services.device_service import (
    DeviceService,
)

from app.repositories.plugin_repository import (
    PluginRepository,
)

from app.core.logger import logger


bus = EventBus()

alarm = AlarmService()
history = HistoryService()
mqtt = MQTTService()
ws = WebSocketService()


bus.subscribe(
    TagChangedEvent,
    alarm.on_tag_changed,
)

bus.subscribe(
    TagChangedEvent,
    history.on_tag_changed,
)

bus.subscribe(
    TagChangedEvent,
    mqtt.on_tag_changed,
)

bus.subscribe(
    TagChangedEvent,
    ws.on_tag_changed,
)


plugin_manager = PluginManager()

driver_factory = DriverFactory(
    plugin_manager
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    logger.info(
        "Starting IoT Gateway..."
    )

    # -----------------------------------------------------
    # Load plugins
    # -----------------------------------------------------

    plugin_manager.initialize()

    # -----------------------------------------------------
    # Runtime services
    # -----------------------------------------------------

    device_manager = DeviceManager(
        bus=bus,
        driver_factory=driver_factory,
    )

    polling_engine = PollingEngine(
        device_manager
    )

    app.state.device_manager = (
        device_manager
    )

    app.state.polling_engine = (
        polling_engine
    )

    app.state.bus = bus

    app.state.driver_factory = (
        driver_factory
    )

    app.state.plugin_manager = (
        plugin_manager
    )

    # -----------------------------------------------------
    # Load devices
    # -----------------------------------------------------

    async with SessionLocal() as session:

        device_service = DeviceService(

            repository=
                DeviceRepository(session),

            plugin_repository=
                PluginRepository(session),

            plugin_manager=
                plugin_manager,
        )

        devices = (
            await device_service.get_all()
        )

        await device_manager.initialize(
            devices
        )

    logger.info(
        "Gateway started."
    )

    try:

        yield

    finally:

        logger.info(
            "Stopping IoT Gateway..."
        )

        await device_manager.shutdown()

        logger.info(
            "Gateway stopped."
        )