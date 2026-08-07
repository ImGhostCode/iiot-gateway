from app.plugins.base import PluginBase
from app.plugins.info import PluginInfo

from app.protocols.simulator.driver import (
    SimulatorDriver,
)


class Plugin(PluginBase):

    info = PluginInfo(

        name="simulator",

        version="1.0.0",

        author="IIoT Gateway",

        description=
            "Built-in device simulator protocol",
    )

    driver = SimulatorDriver

    async def startup(self):
        pass

    async def shutdown(self):
        pass

    async def health(self):
        return True