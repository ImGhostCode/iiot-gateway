from app.gateway.runtime.raw_value import RawValue
from app.plugins.device_context import DeviceContext
from app.plugins.base_driver import BaseDriver

from app.protocols.modbus.client import (
    ModbusClient,
)

from app.protocols.modbus.decoder import (
    ModbusDecoder,
)


class ModbusDriver(BaseDriver):

    def __init__(
        self,
        device,
    ):

        super().__init__(device)

        self.client = None

    async def initialize(self):

        context = DeviceContext(
            self.device
        )

        host = context.require("IP")

        port = int(
            context.get(
                "Port",
                502,
            )
        )

        slave = int(
            context.get(
                "SlaveId",
                1,
            )
        )

        self.client = ModbusClient(
            host=host,
            port=port,
            slave=slave,
        )

    async def connect(self):

        if self.client is None:
            await self.initialize()

        self.connected = (
            await self.client.connect()
        )

        return self.connected

    async def disconnect(self):

        if self.client is not None:

            await self.client.close()

        self.connected = False

    async def read(self):

        if not self.connected:
            return []

        values = []

        for variable in (
            self.device.device_variables
        ):

            response = await self.client.read(
                variable
            )

            if response.isError():
                continue

            decoded = (
                ModbusDecoder.decode(
                    registers=response.registers,
                    data_type=variable.data_type,
                )
            )

            values.append(
                RawValue(
                    variable_id=variable.id,
                    value=decoded,
                )
            )

        return values

    async def write(
        self,
        variable,
        value,
    ):

        raise NotImplementedError(
            "Modbus write is not implemented"
        )