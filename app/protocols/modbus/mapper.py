from enum import Enum
from app.db.models.base import DataTypeEnum

class ModbusArea(str, Enum):
    COIL = "Coil"
    DISCRETE_INPUT = "DiscreteInput"
    HOLDING_REGISTER = "HoldingRegister"
    INPUT_REGISTER = "InputRegister"

class ModbusMapper:
    @staticmethod
    def register_count(data_type):
        match data_type:
            case DataTypeEnum.Bool:
                return 1

            case DataTypeEnum.Int16:
                return 1

            case DataTypeEnum.Uint16:
                return 1

            case DataTypeEnum.Int32:
                return 2

            case DataTypeEnum.Uint32:
                return 2

            case DataTypeEnum.Float:
                return 2

            case DataTypeEnum.Int64:
                return 4

            case DataTypeEnum.Uint64:
                return 4

            case DataTypeEnum.Double:
                return 4

            case _:
                raise ValueError(
                    f"Unsupported data type: {data_type}"
                )