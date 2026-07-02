#!/usr/bin/env python3
"""
Serial Simulator — giả lập Arduino gửi data qua cổng Serial,
dùng để test SerialDriver khi chưa cắm Arduino thật.

Cách dùng (giống Modbus simulator — cần cặp cổng serial ảo):

    Linux/Mac:
        socat -d -d pty,raw,echo=0 pty,raw,echo=0
        → cho ra 2 đường dẫn, vd /dev/pts/5 và /dev/pts/6

        python test_serial_simulator.py /dev/pts/5
        → Gateway .env: SERIAL_PORT=/dev/pts/6

    Windows: dùng com0com tạo cặp CNCA0 <-> CNCB0
        python test_serial_simulator.py CNCA0
        → Gateway .env: SERIAL_PORT=CNCB0

Format gửi đi giống hệt Arduino thật sẽ gửi:
    gas=120.5,soil_moisture=45.2,water_level=12.0
"""

import random
import sys
import time

import serial


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python test_serial_simulator.py <cổng_serial>")
        print("Ví dụ:    python test_serial_simulator.py /dev/pts/5")
        print("Windows:  python test_serial_simulator.py COM7")
        sys.exit(1)

    port = sys.argv[1]

    try:
        ser = serial.Serial(port, baudrate=9600, timeout=1)
    except serial.SerialException as exc:
        print(f"Lỗi mở cổng {port}: {exc}")
        sys.exit(1)

    print(f"Serial Simulator: đang gửi data giả lập qua {port}")
    print("Format: gas=<value>,soil_moisture=<value>,water_level=<value>")
    print("Nhấn Ctrl+C để dừng.\n")

    try:
        while True:
            gas = round(random.uniform(80, 150), 1)
            soil = round(random.uniform(30, 60), 1)
            water = round(random.uniform(5, 20), 1)

            line = f"gas={gas},soil_moisture={soil},water_level={water}\n"
            ser.write(line.encode("utf-8"))
            print(f"  → Gửi: {line.strip()}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nDừng simulator.")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
