from app.plugins.modbus.driver import ModbusDriver
from app.plugins.simulator.driver import SimulatorDriver
from app.gateway.plugin_manager import PluginManager
# from app.plugins.mqtt.driver import MQTTDriver
# from app.plugins.opcua.driver import OpcUaDriver

class DriverFactory:
    # plugin_manager = PluginManager()

# plugin_manager.register(
#     "Simulator",
#     SimulatorDriver,
# )

# plugin_manager.register(
#     "ModbusTcp",
#     ModbusDriver,
# )
    
    @staticmethod
    async def create(device):
        match device.driver.driver_name:
            case "Simulator":
                driver = SimulatorDriver(device)
            case "ModbusTcp":
                driver = ModbusDriver(device)
            case _:
                raise ValueError(
                    f"Unsupported protocol: {device.driver.driver_name}"
                )
        await driver.initialize()

        return driver