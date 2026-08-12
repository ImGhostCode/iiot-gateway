import json

from app.gateway.runtime.raw_value import RawValue
from app.plugins.device_context import DeviceContext
from app.plugins.base_driver import BaseDriver
from app.plugins.config import ConfigParameter

from app.db.models.base import DataSide

from app.protocols.modbus.client import ModbusClient
from app.protocols.modbus.decoder import ModbusDecoder


class ModbusDriver(BaseDriver):

    @classmethod
    def config_schema(cls):

        return [

            ConfigParameter(
                name="IP",
                description="Modbus TCP server IP address",
                default="127.0.0.1",
            ),

            ConfigParameter(
                name="Port",
                description="Modbus TCP server port",
                default="502",
            ),

            ConfigParameter(
                name="SlaveId",
                description="Modbus slave ID",
                default="1",
            ),

        ]

    async def initialize(self):

        ctx = DeviceContext(self.device)

        self.client = ModbusClient(

            host=ctx.require("IP"),

            port=int(
                ctx.get("Port", 502)
            ),

            slave=int(
                ctx.get("SlaveId", 1)
            ),

        )

    async def connect(self):

        self.connected = await self.client.connect()

    async def disconnect(self):

        if self.connected:

            await self.client.close()

        self.connected = False

    async def read(self) -> list[RawValue]:

        values = []

        for variable in self.device.device_variables:

            response = await self.client.read(variable)

            if response.isError():

                continue

            decoded = ModbusDecoder.decode(
                registers=response.registers,
                data_type=variable.data_type,
            )

            values.append(
                RawValue(
                    variable.id,
                    decoded,
                )
            )

        return values

    async def write(
        self,
        variable,
        value,
    ):

        raise NotImplementedError