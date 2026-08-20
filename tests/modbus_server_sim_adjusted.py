import asyncio
import logging

from pymodbus import ModbusDeviceIdentification
from pymodbus.datastore import (
    ModbusDeviceContext,
    ModbusSequentialDataBlock,
    ModbusServerContext,
)
from pymodbus.server import StartAsyncTcpServer


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


# The current ModbusClient passes device_address directly to PyModbus:
#     address=int(variable.device_address)
# Therefore variable addresses are ZERO-BASED.
#
# Holding Registers:
#   0-1  Temperature (Float)
#   2-3  Humidity (Float)
#   4    Soil Moisture (UInt16)
#   9    Motor Speed (UInt16)
#   10   Pressure (Int16)
#
# Coils:
#   0    Pump
#   1    Valve 1
#   2    Valve 2
#   3    Valve 3
#
# Discrete Inputs:
#   0    Water Leak
#   1    Emergency Stop
#
# Input Registers:
#   0    Tank Level
#   1    Flow Rate


async def run_server():
    coils = [False] * 100
    coils[0] = False  # Pump
    coils[1] = True   # Valve 1
    coils[2] = False  # Valve 2
    coils[3] = True   # Valve 3

    discrete_inputs = [False] * 100
    discrete_inputs[0] = False  # Water Leak
    discrete_inputs[1] = True   # Emergency Stop

    holding_registers = [0] * 100

    # Temperature = 25.50
    # IEEE-754 float: 0x41CC0000 -> [0x41CC, 0x0000]
    holding_registers[0] = 0x41CC
    holding_registers[1] = 0x0000

    # Humidity = 44.5
    # IEEE-754 float: 0x42828000 -> [0x4282, 0x8000] 42320000
    holding_registers[2] = 0x4232
    holding_registers[3] = 0x0000

    # Soil Moisture = 6500 -> 65.00% with scale 0.01
    holding_registers[4] = 6500

    # Motor Speed = 1500 RPM
    holding_registers[9] = 1500

    # Pressure = 250 -> 2.50 bar with scale 0.01
    holding_registers[10] = 250

    input_registers = [0] * 100

    # Tank Level = 7500 -> 75.00% with scale 0.01
    input_registers[0] = 7500

    # Flow Rate = 1250 -> 12.50 L/min with scale 0.01
    input_registers[1] = 1250

    store = ModbusDeviceContext(
        di=ModbusSequentialDataBlock(1, discrete_inputs),
        co=ModbusSequentialDataBlock(1, coils),
        ir=ModbusSequentialDataBlock(1, holding_registers),
        hr=ModbusSequentialDataBlock(1, input_registers),
    )

    context = ModbusServerContext(
        devices=store,
        single=True,
    )

    identity = ModbusDeviceIdentification()
    identity.VendorName = "PythonSim"
    identity.ProductCode = "IIOT-MODBUS-TCP"
    identity.VendorUrl = "https://github.com/pymodbus-dev/pymodbus"
    identity.ProductName = "IIoT Gateway Modbus TCP Simulator"
    identity.ModelName = "IIoT Modbus Device Simulator"

    print(">>> Modbus TCP Server")
    print(">>> Address : 127.0.0.1:502")
    print(">>> Unit ID : 1")
    print()
    print("Holding Registers:")
    print("  [0-1]  Temperature = 25.50")
    print("  [2-3]  Humidity    = 44.5")
    print("  [4]    Soil        = 6500")
    print("  [9]    Motor Speed = 1500")
    print("  [10]   Pressure    = 250")
    print()
    print("Coils:")
    print("  [0] Pump   = OFF")
    print("  [1] Valve1 = ON")
    print("  [2] Valve2 = OFF")
    print("  [3] Valve3 = ON")
    print()
    print("Discrete Inputs:")
    print("  [0] Water Leak     = OFF")
    print("  [1] Emergency Stop = ON")
    print()
    print("Input Registers:")
    print("  [0] Tank Level = 7500")
    print("  [1] Flow Rate  = 1250")
    print()
    print(">>> Starting server...")

    await StartAsyncTcpServer(
        context=context,
        identity=identity,
        address=("127.0.0.1", 502),
    )


if __name__ == "__main__":
    asyncio.run(run_server())
