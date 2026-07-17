class DeviceContext:

    def __init__(self, device):
        self.device = device
        self.config = {
            item.device_config_name: item.value
            for item in device.configs
        }

    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def require(self, key):
        value = self.get(key)
        if value is None:
            raise Exception(f"Missing config: {key}")
        return value