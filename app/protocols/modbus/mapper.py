from enum import Enum

class ModbusArea(str, Enum):
    COIL = "Coil"
    DISCRETE_INPUT = "DiscreteInput"
    HOLDING_REGISTER = "HoldingRegister"
    INPUT_REGISTER = "InputRegister"

class ModbusMapper:
    @staticmethod
    def register_count(data_type: str) -> int:
        return {
            "Bool": 1,
            "Int16": 1,
            "UInt16": 1,
            "Int32": 2,
            "UInt32": 2,
            "Float": 2,
            "Int64": 4,
            "UInt64": 4,
            "Double": 4,
            "String": 10,
        }.get(data_type, 1)