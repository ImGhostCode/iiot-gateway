from fastapi import Request
from app.gateway.device_manager import DeviceManager
from app.gateway.polling_engine import PollingEngine
from app.gateway.event_bus import EventBus

def get_device_manager(request: Request) -> DeviceManager:
    return request.app.state.device_manager

def get_polling_engine(request: Request) -> PollingEngine:
    return request.app.state.polling_engine

def get_event_bus(request: Request) -> EventBus:
    return request.app.state.bus