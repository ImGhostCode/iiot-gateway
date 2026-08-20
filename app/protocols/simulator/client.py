import random
from app.db.models.base import (
    DataTypeEnum
)

class SimulatorClient:

    async def read(self, variable):

        match variable.data_type:

            case DataTypeEnum.Bool:
                return random.choice([True, False])

            case DataTypeEnum.Float:
                return round(random.uniform(20, 30), 2)

            case DataTypeEnum.Uint16:
                return random.randint(0, 100)

            case _:
                return 0