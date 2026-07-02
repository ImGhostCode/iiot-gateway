import logging
import threading

import serial

from gateway.config.settings import config
from gateway.core.datapoint import DataPoint
from gateway.drivers.base import BaseDriver

logger = logging.getLogger(__name__)

class SerialDriver(BaseDriver):
    def __init__(self, on_data):
        super().__init__(on_data)
        self._serial: serial.Serial | None = None
        self._read_thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        logger.info(
            f"Serial Driver: open port {config.serial.port} @ {config.serial.baudrate} baud"
        )
        try:
            self._serial = serial.Serial(
                port=config.serial.port,
                baudrate=config.serial.baudrate,
                timeout=2,
            )
        except serial.SerialException as exc:
            logger.error(
                f"Serial Driver: Cannot open port {config.serial.port}: {exc}. "
                f"Please check USB Arduino, or COM name."
            )
            return
        
        self._stop_event.clear()
        self._read_thread = threading.Thread(
            target=self._read_loop, daemon=True, name="serial-read-thread"
        )
        self._read_thread.start()
        logger.info("Serial Driver: Started reading data")

    def stop(self) -> None:
        logger.info("Serial Driver: stopping...")
        self._stop_event.set()
        if self._read_thread is not None:
            self._read_thread.join(timeout=5)
        if self._serial is not None and self._serial.is_open:
            self._serial.close()


    def _read_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                raw_line = self._serial.readline().decode("utf-8", errors='ignore').strip()
                if raw_line:
                    self._parse_line(raw_line)
            except serial.SerialException as exc:
                logger.error(f"Serial Driver: Unknown exception: {exc}")
    
    def _parse_line(self, line: str) -> None:
        try: 
            pairs = [p.strip() for p in line.split(",") if "=" in p]
            print(f"Serial Driver: Received line: {line!r}, parsed pairs: {pairs}")
            if not pairs:
                logger.debug(f"Serial Driver: skipping invalid line format: {line!r}")
                return
            
            for pair in pairs:
                key, _, raw_value = pair.partition("=")
                try:
                    value = float(raw_value)
                except ValueError:
                    logger.warning(
                        f"Serial Driver: Value '{raw_value}' of '{key}' is not a number, skipping" 
                    )
                    continue

                point = DataPoint(
                    device_id=config.serial.device_id,
                    measurement=key.strip(),
                    value=value,
                    protocol="serial"
                )
                self.emit(point)

        except Exception as exc:
            logger.warning(f"Serial Driver: Line parse failed {line!r}: {exc}")