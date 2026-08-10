import asyncio

from app.core.logger import logger

from app.gateway.driver_factory import (
    DriverFactory,
)

from app.gateway.runtime.runtime_builder import (
    RuntimeBuilder,
)

from app.gateway.runtime.runtime_device import (
    RuntimeDevice,
)

from app.gateway.device_worker import (
    DeviceWorker,
)


class DeviceManager:

    def __init__(
        self,
        bus,
        driver_factory: DriverFactory,
    ):

        self.bus = bus

        self.driver_factory = (
            driver_factory
        )

        self.devices: dict[
            str,
            RuntimeDevice
        ] = {}

    async def initialize(
        self,
        devices,
    ):

        logger.info(
            "Initializing %d devices",
            len(devices),
        )

        for device in devices:

            if (
                device.device_type_enum.name
                != "Device"
            ):
                continue

            if not device.auto_start:
                continue

            try:

                await self.start(
                    device
                )

            except Exception as ex:

                logger.exception(
                    "Failed to start device %s: %s",
                    device.device_name,
                    ex,
                )

        logger.info(
            "Initialized %d runtime devices",
            len(self.devices),
        )

    async def start(
        self,
        device,
    ) -> RuntimeDevice:

        device_id = str(device.id)

        existing = self.devices.get(
            device_id
        )

        if existing is not None:

            if existing.connected:
                return existing

            await self.remove(
                device_id
            )

        driver = await (
            self.driver_factory.create(
                device
            )
        )

        runtime = RuntimeBuilder.build(
            device,
            driver,
        )

        await driver.connect()

        runtime.connected = True
        runtime.polling = True

        worker = DeviceWorker(
            runtime,
            self.bus,
        )

        runtime.polling_task = (
            asyncio.create_task(
                worker.start()
            )
        )

        self.devices[
            device_id
        ] = runtime

        logger.info(
            "Device started: %s",
            device.device_name,
        )

        return runtime

    async def stop(
        self,
        device_id,
    ) -> bool:

        runtime = self.devices.get(
            str(device_id)
        )

        if runtime is None:
            return False

        runtime.polling = False

        if runtime.polling_task:

            runtime.polling_task.cancel()

            try:
                await runtime.polling_task

            except asyncio.CancelledError:
                pass

            runtime.polling_task = None

        if runtime.driver.connected:

            await runtime.driver.disconnect()

        runtime.connected = False

        logger.info(
            "Device stopped: %s",
            runtime.device.device_name,
        )

        return True

    async def restart(
        self,
        device,
    ) -> RuntimeDevice:

        await self.remove(
            str(device.id)
        )

        return await self.start(
            device
        )

    async def remove(
        self,
        device_id,
    ) -> bool:

        device_id = str(device_id)

        runtime = self.devices.pop(
            device_id,
            None,
        )

        if runtime is None:
            return False

        runtime.polling = False

        if runtime.polling_task:

            runtime.polling_task.cancel()

            try:
                await runtime.polling_task

            except asyncio.CancelledError:
                pass

        try:

            await runtime.driver.disconnect()

        except Exception:

            logger.exception(
                "Failed to disconnect device %s",
                device_id,
            )

        runtime.connected = False

        logger.info(
            "Device removed from runtime: %s",
            device_id,
        )

        return True

    async def shutdown(self):

        for device_id in list(
            self.devices.keys()
        ):

            await self.remove(
                device_id
            )

        self.devices.clear()

    def get(
        self,
        device_id,
    ):

        return self.devices.get(
            str(device_id)
        )