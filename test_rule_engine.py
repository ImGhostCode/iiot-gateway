#!/usr/bin/env python3
"""
Test Rule Engine — gửi giá trị vượt ngưỡng để trigger alert, đồng thời
subscribe topic iiot/alerts/# để xem alert có được publish không.

Chạy trong 2 terminal:
    Terminal 1: python -m gateway.main
    Terminal 2: python test_rule_engine.py

Script sẽ gửi lần lượt:
    1. Nhiệt độ bình thường (30°C) → không trigger
    2. Nhiệt độ warning (36°C > 35.0) → trigger warning
    3. Nhiệt độ critical (42°C > 40.0) → trigger critical
    4. Gas cao (150 > 130) → trigger critical
    5. RPM âm (-10 < 0) → trigger critical (rule wildcard)
"""

import json
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

alerts_received = []


def on_alert(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    alerts_received.append(payload)
    severity = payload["severity"].upper()
    icon = "🔴" if severity == "CRITICAL" else "🟡"
    print(
        f"\n  {icon} ALERT nhận được trên topic '{msg.topic}':\n"
        f"     Rule     : {payload['rule_name']}\n"
        f"     Device   : {payload['device_id']}\n"
        f"     Giá trị  : {payload['measurement']} = {payload['value']} "
        f"{payload['condition']} {payload['threshold']}\n"
        f"     Severity : {payload['severity']}"
    )


def publish(client, device_id, data: dict):
    import json
    payload = {"device_id": device_id, **data}
    topic = f"iiot/{device_id}/telemetry"
    client.publish(topic, json.dumps(payload), qos=1)
    print(f"  → Gửi: {payload}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="rule-test")
    client.on_message = on_alert
    client.connect(BROKER, PORT)
    client.subscribe("iiot/alerts/#", qos=1)
    client.loop_start()
    time.sleep(0.5)

    print("=" * 58)
    print("  Test Rule Engine — gửi giá trị và chờ alert")
    print("=" * 58)

    test_cases = [
        ("esp32-01", {"temperature": 30.0, "humidity": 55.0},
         "Bình thường — không có alert"),
        ("esp32-01", {"temperature": 36.0, "humidity": 28.0},
         "Nhiệt độ warning + độ ẩm thấp"),
        ("esp32-01", {"temperature": 42.0},
         "Nhiệt độ critical"),
        ("arduino-env-01", {"gas": 150.0, "soil_moisture": 30.0},
         "Gas critical + đất khô warning"),
        ("stm32-plc-01", {"motor_rpm": -10, "motor_temp": 74.0},
         "RPM âm critical + nhiệt độ motor critical"),
    ]

    for device_id, data, description in test_cases:
        print(f"\n[Test] {description}")
        publish(client, device_id, data)
        time.sleep(1.5)  # đợi Gateway xử lý và publish alert

    time.sleep(1)
    print(f"\n{'=' * 58}")
    print(f"  Tổng kết: nhận được {len(alerts_received)} alert(s)")
    print("=" * 58)

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()
