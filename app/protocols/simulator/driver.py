from app.db.models.device import Device

from app.plugins.base_driver import BaseDriver
from app.plugins.config import ConfigParameter

from app.gateway.runtime.raw_value import RawValue

from app.protocols.simulator.client import SimulatorClient


class SimulatorDriver(BaseDriver):

    def __init__(self, device: Device):

        super().__init__(device)

        self.client = SimulatorClient()

    @classmethod
    def config_schema(cls):

        return [

            ConfigParameter(
                name="Generator",
                description="Value generator",
                default="Random",
                enum_info=(
                    '{"Random":0,"Sine":1,"Ramp":2,"Toggle":3}'
                ),
            ),

            ConfigParameter(
                name="Min",
                description="Minimum generated value",
                default="0",
                enum_info=""
            ),

            ConfigParameter(
                name="Max",
                description="Maximum generated value",
                default="100",
                enum_info=""
            ),

            ConfigParameter(
                name="Period",
                description="Generator period in seconds",
                default="10",
                enum_info=""
            ),

        ]

    async def initialize(self):

        pass

    async def connect(self):

        self.connected = True

    async def disconnect(self):

        self.connected = False

    async def read(self) -> list[RawValue]:

        values = []

        for variable in self.device.device_variables:

            value = await self.client.read(variable)

            values.append(
                RawValue(
                    variable.id,
                    value,
                )
            )

        return values

    async def write(
        self,
        variable,
        value,
    ):

        raise NotImplementedError