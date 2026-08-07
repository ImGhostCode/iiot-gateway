from app.plugins.base import PluginBase
from app.plugins.info import (
    ConfigParameterInfo,
    PluginInfo,
)

from app.protocols.modbus.driver import (
    ModbusDriver,
)


class Plugin(PluginBase):

    info = PluginInfo(

        name="modbus",

        version="1.0.0",

        author="IIoT Gateway",

        description="Modbus TCP protocol",

        config_parameters=(

            ConfigParameterInfo(
                name="IP",
                description=
                    "Modbus TCP server IP address",
                data_type="string",
                default="127.0.0.1",
                required=True,
            ),

            ConfigParameterInfo(
                name="Port",
                description=
                    "Modbus TCP server port",
                data_type="integer",
                default=502,
                required=True,
            ),

            ConfigParameterInfo(
                name="SlaveId",
                description=
                    "Modbus slave/unit identifier",
                data_type="integer",
                default=1,
                required=True,
            ),
        ),
    )

    driver = ModbusDriver

    async def startup(self):
        pass

    async def shutdown(self):
        pass

    async def health(self):
        return True