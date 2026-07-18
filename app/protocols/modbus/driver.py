from app.gateway.runtime.raw_value import RawValue
from app.plugins.device_context import DeviceContext
from app.plugins.base_driver import BaseDriver
from app.protocols.modbus.client import ModbusClient
from app.protocols.modbus.decoder import ModbusDecoder

class ModbusDriver(BaseDriver):

    async def initialize(self):
        ctx = DeviceContext(self.device)
        self.client = ModbusClient(
            host=ctx.require("IP"),
            port=int(ctx.get("Port", 502)),
            slave=int(ctx.get("SlaveId", 1))
        )

    async def connect(self):
        self.connected = await self.client.connect()

    async def disconnect(self):
        if self.connected:
           await self.client.close()

    async def read(self) -> list[RawValue]:
        values = []
        for variable in self.device.variables:
            response = await self.client.read(variable)
            if response.isError():
                continue
            decoded = ModbusDecoder.decode(registers=response.registers,data_type= variable.data_type)
            values.append(
                RawValue(variable.id, decoded)
            )
        return values

    async def write(self, variable, value):
        pass