from app.plugins.base import PluginBase


class PluginRegistry:

    def __init__(self):
        self._plugins: dict[str, PluginBase] = {}

    def register(self, plugin: PluginBase):

        name = plugin.info.name.strip().lower()

        if not name:
            raise ValueError(
                "Plugin name cannot be empty"
            )

        if plugin.driver is None:
            raise ValueError(
                f"Plugin '{name}' has no driver"
            )

        self._plugins[name] = plugin

    def get(self, name: str):

        if not name:
            return None

        return self._plugins.get(
            name.strip().lower()
        )

    def all(self):
        return list(
            self._plugins.values()
        )

    def contains(self, name: str) -> bool:

        return self.get(name) is not None