from importlib import import_module
from pathlib import Path

from app.plugins.registry import PluginRegistry

class PluginLoader:
    def __init__(self, registry: PluginRegistry):
        self.registry = registry

    def load(self, plugin_root: Path):
        for folder in plugin_root.iterdir():
            if not folder.is_dir():
                continue
            try:
                module = import_module(
                    f"app.protocols.{folder.name}.plugin"
                )
                plugin = module.Plugin()
                print(f"Loaded plugin: {plugin.info.name}")
                # if plugin.info.name == "":
                #     raise PluginError()

                # if plugin.driver is None:
                #     raise PluginError()
                self.registry.register(plugin)
            except ModuleNotFoundError:
                continue