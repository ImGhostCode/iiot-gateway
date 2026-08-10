from app.db.models.device import Device
from app.plugins.base_driver import BaseDriver
from app.gateway.runtime.raw_value import RawValue
from app.protocols.simulator.client import SimulatorClient
from app.core.logger import logger


class SimulatorDriver(BaseDriver):

    def __init__(
        self,
        device: Device,
    ):
        super().__init__(device)

        self.client = SimulatorClient()

    async def initialize(self):

        # Simulator currently has
        # no configuration requirements.
        pass

    async def connect(self):

        self.connected = True

        return True

    async def disconnect(self):

        self.connected = False

    async def read(
        self,
    ) -> list[RawValue]:
        
        values = []

        for variable in (
            self.device.device_variables
        ):

            value = await self.client.read(
                variable
            )
            

            values.append(
                RawValue(
                    variable_id=variable.id,
                    value=value,
                )
            )

            logger.info("[SimulatorDriver] read value: {variable.id}: {value}" )


        return values

    async def write(
        self,
        variable,
        value,
    ):

        raise NotImplementedError(
            "Simulator write is not implemented"
        )