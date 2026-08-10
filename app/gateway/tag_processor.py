from datetime import datetime, timezone

from app.gateway.data_converter import (
    DataConverter,
)

from app.gateway.expression_engine import (
    ExpressionEngine,
)

from app.gateway.event import (
    TagChangedEvent,
)

from app.gateway.event_bus import EventBus


class TagProcessor:

    def __init__(
        self,
        bus: EventBus,
    ):
        self.bus = bus

    async def process(
        self,
        runtime,
        values,
    ):

        for raw in values:

            variable = runtime.variables.get(
                str(raw.variable_id)
            )

            if variable is None:
                continue

            old_value = variable.value

            converted = (
                DataConverter.convert(
                    variable,
                    raw.value,
                )
            )

            converted = (
                ExpressionEngine.evaluate(
                    variable,
                    converted,
                )
            )

            variable.value = converted

            variable.quality = "Good"

            variable.timestamp = (
                datetime.now(timezone.utc)
            )

            if old_value != variable.value:

                await self.bus.publish(
                    TagChangedEvent(

                        device_id=
                            runtime.device.id,

                        variable_id=
                            variable.id,

                        old_value=
                            old_value,

                        new_value=
                            variable.value,

                        timestamp=
                            variable.timestamp,
                    )
                )