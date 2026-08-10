class DeviceContext:

    def __init__(
        self,
        device,
    ):

        self.device = device

        self.config = {
            config.device_config_name:
                config.value

            for config
            in device.device_configs
        }

    def get(
        self,
        key,
        default=None,
    ):

        return self.config.get(
            key,
            default,
        )

    def require(
        self,
        key,
    ):

        value = self.get(key)

        if value is None:
            raise ValueError(
                f"Missing device configuration: "
                f"{key}"
            )

        return value