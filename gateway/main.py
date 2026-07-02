import logging
import signal
import sys
import time
import os

from gateway.config.settings import config
from gateway.core.influx_writer import InfluxWriter
from gateway.drivers.mqtt_driver import MQTTDriver
from gateway.drivers.modbus_driver import ModbusDriver
from gateway.drivers.serial_driver import SerialDriver

logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s [%(levelname)s %(name)s: %(message)s]",
)
logger = logging.getLogger("gateway.main")

class Gateway:
    def __init__(self):
        self._writer = InfluxWriter()

        self._drivers = [
            MQTTDriver(on_data=self._writer.write),
        ]
        print(os.getenv("MODBUS_ENABLED", "false"))
        print(os.getenv("SERIAL_ENABLED", "false"))
        
        if config.modbus.enabled:
            self._drivers.append(ModbusDriver(on_data=self._writer.write))
        else:
            logger.info("Modbus Driver: disabled")

        if config.serial.enabled:
            self._drivers.append(SerialDriver(on_data=self._writer.write))
        else:
            logger.info("Serial Driver: disabled")
        self._running = False

    def start(self) -> None:
        logger.info("=== Starting IIoT Gateway ===")
        for driver in self._drivers:
            driver.start()
        self._running = True
        logger.info("Gateway is running. Press Ctrl+C to stop.")
    
    def stop(self) -> None:
        logger.info("=== Stopping Gateway ===")
        for driver in self._drivers:
            driver.stop()
        self._writer.close()
        self._running = False
        logger.info("Gateway stopped completely.")
    
    def run_forever(self) -> None:
        self.start()

        def handle_sigterm(signum, frame):
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, handle_sigterm);
        signal.signal(signal.SIGTERM, handle_sigterm)

        while self._running:
            time.sleep(1)

def main():
    gateway = Gateway()
    gateway.run_forever()


if __name__ == "__main__":
    main()