from dataclasses import dataclass


@dataclass(slots=True)
class PluginInfo:

    name: str
    version: str
    author: str
    description: str