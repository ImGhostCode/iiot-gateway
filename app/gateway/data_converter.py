from app.db.models.base import DataTypeEnum

class DataConverter:

    @staticmethod
    def convert(variable, value):

        match variable.data_type:

            case DataTypeEnum.Bool:
                return bool(value)

            case DataTypeEnum.Float:
                return float(value)

            case DataTypeEnum.Int16:
                return int(value)

            case DataTypeEnum.Uint16:
                return int(value)

            case _:
                return value