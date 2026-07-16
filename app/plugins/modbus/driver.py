from app.plugins.base_driver import BaseDriver

class ModbusDriver(BaseDriver):

    async def connect(self):
        print(
            f"Connect {self.device.name}"
        )

    async def disconnect(self):
        print(
            f"Disconnect {self.device.name}"
        )

    async def read(self):
        print(
            f"Reading {self.device.name}"
        )

    async def write(self, variable, value):
        print(
            variable,
            value,
        )