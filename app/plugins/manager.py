from pathlib import Path

from app.plugins.loader import PluginLoader
from app.plugins.registry import PluginRegistry

class PluginManager:

    def __init__(self):
        self.registry = PluginRegistry()
        self.loader = PluginLoader(self.registry)

    def initialize(self):
        self.load_plugins(Path("app/protocols"))

    def load_plugins(self, plugin_dir):
        self.loader.load(plugin_dir)

    def get_driver(self, protocol: str):
        plugin = self.registry.get(protocol)

        if plugin is None:
            raise ValueError(
                f"Unsupported protocol: {protocol}"
            )

        return plugin.driver