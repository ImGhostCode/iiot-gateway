import random

class DataGenerator:

    @staticmethod
    def generate(variable):

        match variable.data_type:

            case "Bool":

                return random.choice([True, False])

            case "Float":

                return round(
                    random.uniform(20, 35),
                    2,
                )

            case "Int16":

                return random.randint(0, 100)

            case "UInt16":

                return random.randint(0, 65535)

            case _:

                return 0