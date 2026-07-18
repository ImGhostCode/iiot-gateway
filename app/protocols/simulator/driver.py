import random
from datetime import datetime, timezone

from app.db.models.device import Device
from app.plugins.base_driver import BaseDriver
from app.gateway.runtime.raw_value import RawValue
from app.protocols.simulator.client import SimulatorClient


class SimulatorDriver(BaseDriver):

    def __init__(self, device: Device):
        super().__init__(device)
        self.client = SimulatorClient()

    async def initialize(self):
        pass

    async def connect(self):

        self.connected = True

    async def disconnect(self):

        self.connected = False

    async def read(self) -> list[RawValue]:
        values = []
        for variable in self.device.variables:
            value = await self.client.read(variable)
            values.append(value)
        return values

    async def write(self, variable, value):
        raise NotImplementedError
