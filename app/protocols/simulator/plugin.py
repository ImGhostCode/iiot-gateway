from .driver import SimulatorDriver
from app.plugins.base import PluginBase
from app.plugins.info import PluginInfo


class Plugin(PluginBase):

    info = PluginInfo(
        name="simulator",
        version="1.0.0",
        author="IIoT Gateway",
        description="Simulator protocol"
    )
    driver = SimulatorDriver

    async def startup(self):
        pass

    async def shutdown(self):
        pass

    async def health(self):
        pass