class DataConverter:

    @staticmethod
    def convert(variable, value):

        match variable.data_type:

            case "Bool":
                return bool(value)

            case "Float":
                return float(value)

            case "Int16":
                return int(value)

            case "UInt16":
                return int(value)

            case _:
                return value