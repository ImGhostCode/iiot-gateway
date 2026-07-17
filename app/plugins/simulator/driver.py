import random
from datetime import datetime, timezone

from app.plugins.base_driver import BaseDriver
from app.gateway.runtime.raw_value import RawValue


class SimulatorDriver(BaseDriver):

    async def initialize(self):
        pass

    async def connect(self):

        self.connected = True

    async def disconnect(self):

        self.connected = False

    # async def read(self):

    #     values = []

    #     for variable in self.device.variables:

    #         runtime = self.runtime.variables[
    #             variable.id
    #         ]

    #         match variable.data_type:

    #             case "Bool":

    #                 runtime.value = random.choice(
    #                     [True, False]
    #                 )

    #             case "Float":

    #                 runtime.value = round(
    #                     random.uniform(20, 30),
    #                     2,
    #                 )

    #             case "Int16":

    #                 runtime.value = random.randint(
    #                     0,
    #                     100,
    #                 )

    #             case _:

    #                 runtime.value = 0

    #         runtime.timestamp = datetime.now(timezone.utc)

    #         runtime.quality = "Good"

    #     return self.runtime.variables


    async def read(self):

        values = []

        for variable in self.device.variables:

            match variable.data_type:

                case "Bool":
                    value = random.choice([True, False])

                case "Float":
                    value = round(
                        random.uniform(20, 35),
                        2,
                    )

                case "Int16":
                    value = random.randint(0, 100)

                case _:
                    value = 0

            values.append(
                RawValue(
                    variable.id,
                    value,
                )
            )

        return values

    async def write(self, variable, value):
        raise NotImplementedError
