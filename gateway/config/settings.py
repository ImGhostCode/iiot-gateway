import os
from dataclasses import dataclass, field

@dataclass
class MQTTConfig:
    broker_host: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    broker_port: int = os.getenv("MQTT_BROKER_PORT", 1883)
    # Examples: iiot/esp32-01/telemetry, iiot/esp8266-02/telemetry
    topic_pattern: str = os.getenv("MQTT_TOPIC_PATTERN", "iiot/+/telemetry")
    client_id: str = os.getenv("MQTT_CLIENT_ID", "iiot-gateway-core")
    keepalive: int = 60

@dataclass
class ModbusConfig:
    enabled: bool = os.getenv("MODBUS_ENABLED", "false").lower() == "true"
    port: str = os.getenv("MODBUS_PORT", "/dev/ttyUSB0") # Windows: "COM4" 
    baudrate: int = int(os.getenv("MODBUS_BAUDRATE", "9600"))
    slave_id: int = int(os.getenv("MODBUS_SLAVE_ID", "1"))
    poll_interval_sec: float = float(os.getenv("MODBUS_POLL_INTERVAL", "2.0"))
    device_id: str = os.getenv("MODBUS_DEVICE_ID", "stm32-plc-01")

    # Map: measurement -> Modbus register address (holding register)
    register_map: dict = field(
        default_factory=lambda: {
            "motor_rpm": 0,
            "motor_temp": 1,
            "pressure": 2,
        }
    )

@dataclass
class SerialConfig:
    enabled: bool = os.getenv("SERIAL_ENABLED", "false").lower() == "true"
    port: str = os.getenv("SERIAL_PORT", "/dev/ttyACM0") # Windows: "COM3" 
    baudrate: int = int(os.getenv("SERIAL_BAUDRATE", "9600"))
    device_id: str = os.getenv("SERIAL_DEVICE_ID", "arduino-env-01")



@dataclass
class InfluxDBConfig:
    url: str = os.getenv("INFLUXDB_URL", "http://localhost:8086")
    token: str = os.getenv("INFLUXDB_TOKEN", "my-super-secret-admin-token")
    org: str = os.getenv("INFLUXDB_ORG", "iiot-org")
    bucket: str = os.getenv("INFLUXDB_BUCKET", "gateway-data")
    
@dataclass
class GatewatConfig:
    mqtt: MQTTConfig = field(default_factory=MQTTConfig)
    modbus: ModbusConfig = field(default_factory=ModbusConfig)
    serial: SerialConfig = field(default_factory=SerialConfig)
    infuxdb: InfluxDBConfig = field(default_factory=InfluxDBConfig)
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

config = GatewatConfig()