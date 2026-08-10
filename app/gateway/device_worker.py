import asyncio
from datetime import datetime, timezone

from app.gateway.tag_processor import (
    TagProcessor,
)


class DeviceWorker:

    def __init__(
        self,
        runtime,
        bus,
    ):

        self.runtime = runtime

        self.processor = (
            TagProcessor(bus)
        )

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            try:

                if not (
                    self.runtime.driver.connected
                ):

                    self.runtime.statistics.reconnect_count += 1

                    await (
                        self.runtime.driver
                        .connect()
                    )

                    self.runtime.connected = True

                values = await (
                    self.runtime.driver.read()
                )

                await self.processor.process(
                    self.runtime,
                    values,
                )

                stats = (
                    self.runtime.statistics
                )

                stats.read_count += 1

                stats.last_poll = (
                    datetime.now(timezone.utc)
                )

                self.runtime.connected = True

            except asyncio.CancelledError:

                raise

            except Exception as ex:

                self.runtime.connected = False

                stats = (
                    self.runtime.statistics
                )

                stats.error_count += 1
                stats.last_error = str(ex)

                await asyncio.sleep(5)

                continue

            await asyncio.sleep(
                max(
                    self.runtime.device.enforce_period,
                    100,
                ) / 1000
            )

    def stop(self):

        self.running = False