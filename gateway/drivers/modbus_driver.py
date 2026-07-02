import logging
import threading
import time

from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

from gateway.config.settings import config
from gateway.core.datapoint import DataPoint
from gateway.drivers.base import BaseDriver

logger = logging.getLogger(__name__)

class ModbusDriver(BaseDriver):
    def __init__(self, on_data):
        super().__init__(on_data)
        self._client = ModbusSerialClient(
            port=config.modbus.port,
            baudrate=config.modbus.baudrate,
            timeout=1
        )
        self._poll_thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        logger.info(
            f"Modbus Driver: connecting to {config.modbus.port}"
            f"@ {config.modbus.baudrate} baud, slave_id={config.modbus.slave_id}"
        )

        if not self._client.connect():
            logger.error(
                f"Modbus Driver: Cannot connect to {config.modbus.port}. "
                "Please check RS485 wires for COM name."
            )

            return
        
        self._stop_event.clear()
        self._poll_thread = threading.Thread(
            target=self._poll_loop, daemon=True, name="modbus-poll-thread"
        )
        self._poll_thread.start()
        logger.info("Modbus Driver: Poll loop started")

    def stop(self) -> None:
        logger.info("Modbus Driver: stopping...")
        self._stop_event.set()
        if self._poll_thread is not None:
            self._poll_thread.join(timeout=5)
        self._client.close()

    def _poll_loop(self) -> None:
        while not self._stop_event.is_set():
            self._poll_once()
            self._stop_event.wait(config.modbus.poll_interval_sec)

    def _poll_once(self) -> None:
        for measurement, register_addr in config.modbus.register_map.items():
            try:
                result = self._client.read_holding_registers(
                    address=register_addr,
                    device_id = config.modbus.slave_id,
                    count=1,
                )
                if result.isError():
                    logger.warning(
                        f"Modbus Driver: Register reading failed {register_addr}"
                        f"({measurement}): {result}"
                    )
                    continue

                raw_value = result.registers[0]

                point = DataPoint(
                    device_id=config.modbus.device_id,
                    measurement=measurement,
                    value=float(raw_value),
                    protocol="modbus",
                )
                self.emit(point)
            except ModbusException as exc:
                logger.error(f"Modbus Driver: Reading exception {measurement}: {exc}")
            except Exception as exc:
                logger.error(f"Modbus Driver: Unknown exception: {exc}")
