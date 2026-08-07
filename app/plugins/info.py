from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class ConfigParameterInfo:
    name: str
    description: str
    data_type: str = "string"
    default: Any = None
    required: bool = False
    enum_values: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class PluginInfo:
    name: str
    version: str
    author: str
    description: str
    config_parameters: tuple[ConfigParameterInfo, ...] = ()