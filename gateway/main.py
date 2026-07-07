import logging
import signal
import sys
import threading
import time

import paho.mqtt.client as mqtt
import uvicorn

from gateway.api import routes as api
from gateway.config.settings import config
from gateway.core.influx_writer import InfluxWriter
from gateway.core.rule_engine import RuleEngine
from gateway.core.store import AlertStore, DeviceStore, init_db
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
        self._db = init_db()

        self._device_store = DeviceStore(self._db)
        self._alert_store = AlertStore(self._db)

        self._writer = InfluxWriter()

        self._alert_client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id="iiot_gateway_alert"
        )
        self._alert_client.connect(
            config.mqtt.broker_host,
            int(config.mqtt.broker_port)
        )
        self._alert_client.loop_start()

        self._rule_engine = RuleEngine(
            rules_path=config.rules_path,
            mqtt_client=self._alert_client,
            alert_store=self._alert_store,

        )

        api.init(self._device_store, self._alert_store, self._rule_engine)

        def _on_data(point):
            self._device_store.update(point)
            self._rule_engine.evaluate(point)
            self._writer.write(point)

        self._drivers = [
            MQTTDriver(on_data=_on_data),
        ]

        if config.modbus.enabled:
            self._drivers.append(ModbusDriver(on_data=self._writer.write))
        else:
            logger.info("Modbus Driver: disabled")

        if config.serial.enabled:
            self._drivers.append(SerialDriver(on_data=self._writer.write))
        else:
            logger.info("Serial Driver: disabled")

        self._running = False
        self._api_thread: threading.Thread | None = None
    
    def _start_api(self) -> None:
        uvicorn.run(
            api.app,
            host=config.api_host,
            port=config.api_port,
            log_level="warning"
        )

    def start(self) -> None:
        logger.info("=== Starting IIoT Gateway ===")
        for driver in self._drivers:
            driver.start()

        self._api_thread = threading.Thread(
            target=self._start_api, daemon=True, name="api-thread"
        )    
        self._api_thread.start()
        logger.info(f"REST API: http://{config.api_host}:{config.api_port}/docs")
        
        self._running = True
        logger.info("Gateway is running. Press Ctrl+C to stop.")
    
    def stop(self) -> None:
        logger.info("=== Stopping Gateway ===")
        for driver in self._drivers:
            driver.stop()
        self._writer.close()
        self._alert_client.loop_stop()
        self._alert_client.disconnect()
        self._db.close()
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