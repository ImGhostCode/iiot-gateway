from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.gateway.device_manager import DeviceManager
from app.gateway.polling_engine import PollingEngine

device_manager = DeviceManager()
polling_engine = PollingEngine(device_manager)

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting IoT Gateway...")

    await device_manager.initialize()

    await polling_engine.start()

    yield

    print("Stoping IoT Gateway...")

    await polling_engine.stop()

    await device_manager.shutdown()



