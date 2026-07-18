from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class RuntimeStatistics:

    read_count: int = 0

    error_count: int = 0

    reconnect_count: int = 0

    last_poll: datetime | None = None

    last_error: str | None = None