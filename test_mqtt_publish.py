#!/usr/bin/env python3
"""
Script test nhanh: giả lập 1 device gửi data lên MQTT broker.
Dùng để verify Docker stack (Mosquitto) đã chạy đúng trước khi
viết Gateway core thật.

Cài đặt:
    pip install paho-mqtt

Chạy:
    python test_mqtt_publish.py
"""

import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iiot/test-device/telemetry"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"[OK] Đã kết nối tới Mosquitto broker tại {BROKER_HOST}:{BROKER_PORT}")
    else:
        print(f"[LỖI] Kết nối thất bại, mã lỗi: {reason_code}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect

    print(f"Đang kết nối tới {BROKER_HOST}:{BROKER_PORT} ...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    time.sleep(1)  # đợi connect xong

    try:
        print(f"Bắt đầu publish dữ liệu giả lập lên topic '{TOPIC}'")
        print("Nhấn Ctrl+C để dừng.\n")

        while True:
            payload = {
                "device_id": "test-device-01",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "temperature": round(random.uniform(25.0, 35.0), 2),
                "humidity": round(random.uniform(40.0, 70.0), 2),
            }
            client.publish(TOPIC, json.dumps(payload), qos=1)
            print(f"  → Gửi: {payload}")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nDừng publish.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
