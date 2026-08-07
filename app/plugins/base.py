from .info import PluginInfo


class PluginBase:

    info: PluginInfo
    driver: type

    async def startup(self):
        pass

    async def shutdown(self):
        pass

    async def health(self):
        return True