from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(slots=True)
class RuntimeVariable:

    id: str

    name: str

    data_type: str

    expression: str = None

    value: object = None

    quality: str = "Unknown"

    timestamp: datetime | None = None