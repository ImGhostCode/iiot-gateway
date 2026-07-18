from pymodbus.client import AsyncModbusTcpClient

from .mapper import ModbusArea
from .mapper import ModbusMapper

class ModbusClient:
    def __init__(self, host, port, slave):
        self.client = AsyncModbusTcpClient(host, port=port)
        self.slave = slave
    
    async def connect(self):
        return await self.client.connect()
    
    async def close(self):
        self.client.close()

    async def read(self, variable):
        count = ModbusMapper.register_count(variable.data_type)
        match variable.method:
            case ModbusArea.COIL:
                return await self.client.read_coils(
                    address=int(variable.device_address),
                    count=count,
                    device_id=self.slave
                )
            case ModbusArea.DISCRETE_INPUT:
                return await self.client.read_discrete_inputs(
                    address=int(variable.device_address),
                    count=count,
                    device_id=self.slave
                )
            case ModbusArea.HOLDING_REGISTER:
                return await self.client.read_holding_registers(
                    address=int(variable.device_address),
                    count=count,
                    device_id=self.slave
                )
            case ModbusArea.INPUT_REGISTER:
                return await self.client.read_input_registers(
                    address=int(variable.device_address),
                    count=count,
                    device_id=self.slave
                )
        raise ValueError(variable.method)