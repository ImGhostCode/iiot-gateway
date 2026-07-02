import json
import logging
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

from gateway.config.settings import config
from gateway.core.datapoint import DataPoint
from gateway.drivers.base import BaseDriver

logger = logging.getLogger(__name__)

_RESERVED_KEYS = {"device_id", "timestamp"}

class MQTTDriver(BaseDriver):
    def __init__(self, on_data):
        super().__init__(on_data)
        self._client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=config.mqtt.client_id
        )
        self._client.on_connect = self._handle_connect
        self._client.on_message = self._handle_message
        self._client.on_disconnect = self._handle_disconnect

    def start(self) -> None:
        logger.info(
            f"MQTT Driver: connecting to {config.mqtt.broker_host}:{config.mqtt.broker_port}"
        )
        self._client.connect(
            config.mqtt.broker_host,
            int(config.mqtt.broker_port),
            keepalive=config.mqtt.keepalive
        )
        self._client.loop_start()

    def stop(self) -> None:
        logger.info("MQTT Driver: stopping...")
        self._client.loop_stop()
        self._client.disconnect()


    def _handle_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            client.subscribe(config.mqtt.topic_pattern, qos=1)
            logger.info(
                f"MQTT Driver: connected, subscribe '{config.mqtt.topic_pattern}'"
            )
        else:
            logger.error(f"MQTT Driver: connection failed, error code {reason_code}")

    def _handle_disconnect(self, client, userdata, *args):
        logger.warning("MQTT Driver: disconnected to broker")

    def _handle_message(self, client, userdata, msg) -> None:
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            logger.info(f"MQTT Driver: received payload: {payload}")
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.warning(f"MQTT Driver: invalid payload JSON on {msg.topic}: {exc}")
            return
        
        device_id = payload.get("device_id")
        if not device_id:
            logger.warning(f"MQTT Driver: 'device_id' is required on topic {msg.topic}")
            return
        
        timestamp = self._parse_timestamp(payload.get("timestamp"))

        for key, val in payload.items():
            if key in _RESERVED_KEYS:
                continue
            if not isinstance(val, (int, float)):
                 continue
            
            point = DataPoint(
                device_id=device_id,
                measurement=key,
                value=float(val),
                protocol="mqtt",
                timestamp=timestamp,
            )
            self.emit(point)
    
    @staticmethod
    def _parse_timestamp(raw:str | None) -> datetime:
        if not raw:
            return datetime.now(timezone.utc)
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return datetime.now(timezone.utc) 


