from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(slots=True)
class RuntimeVariable:

    id: int

    name: str

    value: object = None

    quality: str = "Unknown"

    timestamp: datetime | None = None