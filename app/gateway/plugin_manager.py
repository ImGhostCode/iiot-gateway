from typing import Type

from app.plugins.base_driver import BaseDriver

class PluginManager:
    def __init__(self) -> None:
        self._drivers: dict[str, Type[BaseDriver]] = {}

    def register(self, name: str, driver: Type[BaseDriver]):
        self._drivers[name] = driver

    def create(self, name: str, device):
        cls = self._drivers.get(name)
        if cls is None:
            raise ValueError(f"Driver {name} not found.")
        
        return cls(device)