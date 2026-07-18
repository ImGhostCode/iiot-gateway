from app.protocols.modbus.driver import ModbusDriver
from app.plugins.base import PluginBase
from app.plugins.info import PluginInfo


class Plugin(PluginBase):

    info = PluginInfo(
        name="modbus",
        version="1.0.0",
        author="IIoT Gateway",
        description="Modbus TCP protocol"
    )
    driver = ModbusDriver

    async def startup(self):
        pass

    async def shutdown(self):
        pass

    async def health(self):
        pass