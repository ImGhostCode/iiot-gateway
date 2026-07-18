from app.plugins.base import PluginBase

class PluginRegistry:
    def __init__(self):
        self._plugins: dict[str, PluginBase] = {}
    
    def register(self, plugin: PluginBase):
        self._plugins[plugin.info.name] = plugin

    def get(self, name: str):
        return self._plugins.get(name)
    
    def all(self):
        return list(self._plugins.values())