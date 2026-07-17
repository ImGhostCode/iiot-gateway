from pymodbus.client import AsyncModbusTcpClient

from app.plugins.device_context import DeviceContext
from app.plugins.base_driver import BaseDriver

class ModbusDriver(BaseDriver):

    async def initialize(self):
        ctx = DeviceContext(self.device)
        self.host = ctx.require("IP")
        self.port = int(
            ctx.get("Port", 502)
        )
        self.slave = int(
            ctx.get("SlaveId", 1)
        )

    async def connect(self):
        self.client = AsyncModbusTcpClient(
            self.host,
            port=self.port
        )

        self.connected = await self.client.connect()

    async def disconnect(self):
        if self.connected:
            self.client.close()

    async def read(self):
        print(self.device.device_name)

    async def write(self, variable, value):
        pass