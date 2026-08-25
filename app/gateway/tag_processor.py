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

            old_value = variable.cooked_value

            try:

                # -------------------------------------------------
                # 1. Raw value from driver
                # -------------------------------------------------

                raw_value = raw.value

                # -------------------------------------------------
                # 2. Convert raw value according to variable config
                # -------------------------------------------------

                converted = DataConverter.convert(
                    variable,
                    raw_value,
                )

                # -------------------------------------------------
                # 3. Apply expression
                # -------------------------------------------------

                cooked_value = ExpressionEngine.evaluate(
                    variable,
                    converted,
                )

                # -------------------------------------------------
                # 4. Update runtime state
                # -------------------------------------------------

                variable.value = raw_value

                variable.cooked_value = cooked_value

                variable.message = None

                variable.quality = "Good"

                variable.timestamp = (
                    datetime.now(timezone.utc)
                )

                # -------------------------------------------------
                # 5. Publish event when cooked value changes
                # -------------------------------------------------

                if old_value != variable.cooked_value:

                    await self.bus.publish(
                        TagChangedEvent(

                            device_id=runtime.device.id,

                            variable_id=variable.id,

                            old_value=old_value,

                            new_value=variable.cooked_value,

                            timestamp=variable.timestamp,
                        )
                    )

            except Exception as ex:

                variable.message = str(ex)

                variable.quality = "Bad"

                variable.timestamp = (
                    datetime.now(timezone.utc)
                )