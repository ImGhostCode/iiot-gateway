from app.protocols.modbus.driver import ModbusDriver
from app.protocols.simulator.driver import SimulatorDriver
from app.plugins.manager import PluginManager
# from app.plugins.mqtt.driver import MQTTDriver
# from app.plugins.opcua.driver import OpcUaDriver

class DriverFactory:

    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager

    # plugin_manager = PluginManager()

# plugin_manager.register(
#     "Simulator",
#     SimulatorDriver,
# )

# plugin_manager.register(
#     "ModbusTcp",
#     ModbusDriver,
# )
    
    async def create(self, device):
        # match device.driver.driver_name:
        #     case "Simulator":
        #         driver = SimulatorDriver(device)
        #     case "ModbusTcp":
        #         driver = ModbusDriver(device)
        #     case _:
        #         raise ValueError(
        #             f"Unsupported protocol: {device.driver.driver_name}"
        #         )
        # await driver.initialize()

        # return driver

        # plugin = registry.get(device.protocol)
        # driver = plugin.driver(device)
        # return driver
        driver_cls = self.plugin_manager.get_driver(
            device.protocol
        )

        return driver_cls(device)