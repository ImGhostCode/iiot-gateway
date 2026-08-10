from app.plugins.manager import PluginManager


class DriverFactory:

    def __init__(
        self,
        plugin_manager: PluginManager,
    ):
        self.plugin_manager = plugin_manager

    async def create(
        self,
        device,
    ):

        if device.driver is None:

            raise ValueError(
                f"Device '{device.device_name}' "
                "has no driver"
            )

        driver_name = (
            device.driver.driver_name
        )

        driver_cls = (
            self.plugin_manager.get_driver(
                driver_name
            )
        )

        driver = driver_cls(device)

        await driver.initialize()

        return driver