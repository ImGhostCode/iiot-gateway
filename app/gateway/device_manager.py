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
            f"Initializing {len(devices)} devices"
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
                    f"Failed to start device {device.device_name}: {ex}"
                )

        logger.info(
            f"Initialized {len(self.devices)} runtime devices"
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
            f"Device started: {device.device_name}"
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
            f"Device stopped: {runtime.device.device_name}"
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
                f"Failed to disconnect device {device_id}"
            )

        runtime.connected = False

        logger.info(
            "Device removed from runtime: {device_id}"
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