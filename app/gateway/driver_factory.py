from app.plugins.modbus.driver import ModbusDriver
# from app.plugins.mqtt.driver import MQTTDriver
# from app.plugins.opcua.driver import OpcUaDriver

class DriverFactory:
    
    @staticmethod
    def create(device):
        protocol = device.protocol.lower()
    
        match protocol:
            case "modbus":
                return ModbusDriver(device)
            case _:
                raise ValueError(
                    f"Unsupported protocol: {device.protocol}"
                )