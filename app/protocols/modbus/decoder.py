import struct
from app.db.models.base import DataTypeEnum

class ModbusDecoder:

    @staticmethod 
    def decode(registers, data_type):
        if data_type == DataTypeEnum.Uint16:
            return registers[0]
        if data_type == DataTypeEnum.Int16:
            value = registers[0]
            if value > 32767:
                value -= 65536
            return value
        
        if data_type == DataTypeEnum.Float:
            raw = struct.pack(
                ">HH",
                registers[0],
                registers[1]
            )
            return struct.unpack(">f", raw)[0]
        
        return registers
        