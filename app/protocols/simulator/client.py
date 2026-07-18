import random


class SimulatorClient:

    async def read(self, variable):

        match variable.data_type:

            case "Bool":
                return random.choice([True, False])

            case "Float":
                return round(random.uniform(20, 30), 2)

            case "Int16":
                return random.randint(0, 100)

            case _:
                return 0