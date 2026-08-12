from pymodbus.client import ModbusTcpClient

# Connect tới Modbus TCP Server
client = ModbusTcpClient('127.0.0.1', port=502)

if client.connect():
    print("--- Kết nối thành công! ---")

    # 1. Đọc 3 thanh ghi Holding Registers từ địa chỉ 0
    response = client.read_holding_registers(address=0, count=3)
    if not response.isError():
        print(f"Giá trị Holding Registers ban đầu (0-2): {response.registers}")

    # 2. Ghi giá trị 999 vào Holding Register tại địa chỉ 0
    client.write_register(address=0, value=999)
    print("Đã ghi 999 vào thanh ghi 0.")

    # 3. Đọc lại để kiểm tra xem đã cập nhật chưa
    response = client.read_holding_registers(address=0, count=3)
    if not response.isError():
        print(f"Giá trị Holding Registers sau khi ghi: {response.registers}")

    # Ngắt kết nối
    client.close()
else:
    print("Không thể kết nối tới Server!")