from dataclasses import dataclass, field

from app.db.models.device import Device
from app.plugins.base_driver import BaseDriver

from app.gateway.runtime.runtime_variable import RuntimeVariable

@dataclass(slots=True)
class RuntimeDevice:

    # def __init__(self, device: Device, driver: BaseDriver):
    #     self.device = device
    #     self.driver = driver
    #     self.connected = False
    #     self.variables = {}

    device: Device

    driver: BaseDriver

    connected: bool = False

    polling: bool = False

    variables: dict[int, RuntimeVariable] = field(default_factory=dict)

    last_error: str | None = None
        