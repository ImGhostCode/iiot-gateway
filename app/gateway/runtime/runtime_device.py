from dataclasses import dataclass, field
from asyncio import Task

from app.db.models.device import Device
from app.plugins.base_driver import BaseDriver

from app.gateway.runtime.runtime_variable import RuntimeVariable
from app.gateway.runtime.runtime_statistics import RuntimeStatistics

@dataclass(slots=True)
class RuntimeDevice:

    device: Device

    driver: BaseDriver

    connected: bool = False

    polling_task: Task | None = None

    reconnect_task: Task | None = None

    polling: bool = False

    variables: dict[int, RuntimeVariable] = field(default_factory=dict)

    last_error: str | None = None

    statistics: RuntimeStatistics = field(default_factory=RuntimeStatistics)

    
        