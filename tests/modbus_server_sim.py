import logging
from pymodbus.server import StartAsyncTcpServer
from pymodbus import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusDeviceContext
import asyncio

# Bật logging để theo dõi các kết nối và dữ liệu nhận/gửi
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

async def run_server():
    # 1. Khởi tạo vùng nhớ (Data Store)
    # Khởi tạo giá trị ban đầu cho các thanh ghi (bắt đầu từ địa chỉ 0)
    store = ModbusDeviceContext(
        di=ModbusSequentialDataBlock(1, [1, 0, 1, 1]),        # Discrete Inputs (Read-only Bit)
        co=ModbusSequentialDataBlock(1, [0, 0, 0, 0]),        # Coils (Read/Write Bit)
        hr=ModbusSequentialDataBlock(1, [100, 200, 300]),     # Holding Registers (Read/Write Word)
        ir=ModbusSequentialDataBlock(1, [10, 20, 30])         # Input Registers (Read-only Word)
    )
    
    # Context chứa các slave ID, ở đây dùng single=True áp dụng cho mọi Slave ID
    context = ModbusServerContext(devices=store, single=True)

    # 2. (Tùy chọn) Thêm thông tin thiết bị
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'PythonSim'
    identity.ProductCode = 'SIM01'
    identity.VendorUrl = 'https://github.com/pymodbus-dev/pymodbus'
    identity.ProductName = 'Modbus TCP Simulator'
    identity.ModelName = 'Modbus Server'

    # 3. Chạy Server tại 127.0.0.1:502
    print(">>> Modbus TCP Server đang chạy tại 127.0.0.1:502 ...")
    await StartAsyncTcpServer(
        context=context,
        identity=identity,
        address=("127.0.0.1", 502)
    )

if __name__ == "__main__":
    asyncio.run(run_server())