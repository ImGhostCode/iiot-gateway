from pathlib import Path

from app.plugins.loader import PluginLoader
from app.plugins.registry import PluginRegistry


class PluginManager:

    def __init__(self):

        self.registry = PluginRegistry()

        self.loader = PluginLoader(
            self.registry
        )

        self.initialized = False

    def initialize(self):

        if self.initialized:
            return

        plugin_dir = (
            Path(__file__)
            .resolve()
            .parents[1]
            / "protocols"
        )

        self.load_plugins(
            plugin_dir
        )

        self.initialized = True

    def load_plugins(
        self,
        plugin_dir: Path,
    ):

        self.loader.load(
            plugin_dir
        )

    def get_plugin(
        self,
        name: str,
    ):

        return self.registry.get(
            name
        )

    def get_driver(
        self,
        protocol: str,
    ):

        plugin = self.get_plugin(
            protocol
        )

        if plugin is None:

            raise ValueError(
                f"Unsupported protocol: {protocol}"
            )

        return plugin.driver

    def all(self):

        return self.registry.all()

    def available(self):

        return [

            {
                "name": plugin.info.name,

                "version": plugin.info.version,

                "author": plugin.info.author,

                "description":
                    plugin.info.description,

                "driver":
                    f"{plugin.driver.__module__}."
                    f"{plugin.driver.__name__}",
            }

            for plugin
            in self.all()
        ]