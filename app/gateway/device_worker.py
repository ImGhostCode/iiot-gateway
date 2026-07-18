import asyncio
from datetime import datetime, timezone

from app.gateway.tag_processor import TagProcessor


class DeviceWorker:

    def __init__(
        self,
        runtime,
        bus,
    ):

        self.runtime = runtime
        self.processor = TagProcessor(bus)
        self.running = False

    async def start(self):
        self.running = True
        while self.running:
            try:
                if not self.runtime.driver.connected:
                    await self.runtime.driver.connect()
                values = await self.runtime.driver.read()
                await self.processor.process(
                    self.runtime,
                    values,
                )
                self.runtime.statistics.read_count += 1
                self.runtime.statistics.last_poll = datetime.now(timezone.utc)

            except Exception as ex:
                self.runtime.statistics.error_count += 1
                self.runtime.statistics.last_error = str(ex)
                await asyncio.sleep(5)
            await asyncio.sleep(
                self.runtime.device.enforce_period / 1000
            )

    def stop(self):
        self.running = False