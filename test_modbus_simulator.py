#!/usr/bin/env python3
"""
Modbus RTU Slave Simulator — giả lập STM32 để test ModbusDriver
khi chưa có hardware thật / chưa có USB-RS485.

Cách dùng:
    1. Cài thư viện ảo hoá cổng COM (chỉ cần làm 1 lần):

       Linux/Mac: dùng socat để tạo cặp cổng serial ảo
           pip install pymodbus
           socat -d -d pty,raw,echo=0 pty,raw,echo=0
           → socat in ra 2 đường dẫn kiểu /dev/pts/3 và /dev/pts/4
           → dùng 1 cái cho simulator (script này), 1 cái cho MODBUS_PORT trong .env

       Windows: dùng com0com (virtual COM port pair), tạo CNCA0 <-> CNCB0
           → simulator dùng CNCA0, Gateway .env dùng CNCB0

    2. Chạy simulator:
       python test_modbus_simulator.py /dev/pts/3
       (hoặc python test_modbus_simulator.py COM_ẢO trên Windows)

    3. Set .env: MODBUS_ENABLED=true, MODBUS_PORT=<cổng còn lại>
    4. Chạy Gateway: python -m gateway.main

Simulator sẽ random giá trị register mỗi 2 giây để giả lập
motor_rpm, motor_temp, pressure — đúng với register_map mặc định
trong gateway/config/settings.py.

NOTE: Nếu bạn chưa muốn cài socat/com0com, cách đơn giản nhất là
TẠM THỜI giữ MODBUS_ENABLED=false và quay lại bước này sau khi
có STM32 + USB-RS485 thật — ModbusDriver sẽ hoạt động y hệt vì
cùng dùng chuẩn Modbus RTU.
"""

import random
import sys
import time

from pymodbus.server import StartSerialServer
from pymodbus.simulator.simdata import SimData
from pymodbus.simulator.simdevice import SimDevice
from pymodbus.simulator.simutils import DataType


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python test_modbus_simulator.py <cổng_serial>")
        print("Ví dụ:    python test_modbus_simulator.py /dev/pts/3")
        print("Windows:  python test_modbus_simulator.py COM5")
        sys.exit(1)

    port = sys.argv[1]

    # Holding registers: address 0=motor_rpm, 1=motor_temp, 2=pressure
    # khớp với register_map trong gateway/config/settings.py
    initial_values = [1500, 65, 320] + [0] * 7  # 10 registers total
    data = SimData(address=0, values=initial_values, datatype=DataType.REGISTERS)
    context = SimDevice(id=1, simdata=data)

    print(f"Modbus Simulator: đang lắng nghe trên {port} (slave_id=1, baudrate=9600)")
    print("Giả lập register: [0]=motor_rpm [1]=motor_temp [2]=pressure")
    print("Nhấn Ctrl+C để dừng.\n")

    # Random hoá giá trị mỗi vài giây để giống thiết bị thật đang chạy
    import threading

    def randomize_loop():
        while True:
            data.values[0] = random.randint(1400, 1600)  # motor_rpm
            data.values[1] = random.randint(60, 75)       # motor_temp
            data.values[2] = random.randint(300, 340)     # pressure
            time.sleep(3)

    threading.Thread(target=randomize_loop, daemon=True).start()

    StartSerialServer(context=context, port=port, baudrate=9600)


if __name__ == "__main__":
    main()
