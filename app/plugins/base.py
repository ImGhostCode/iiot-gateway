from abc import ABC
from .info import PluginInfo
class PluginBase:

    info: PluginInfo
    driver: type

    async def startup(self):
        """Called when gateway starts."""

    async def shutdown(self):
        """Called when gateway stops."""

    async def health(self):
        """Optional health check."""