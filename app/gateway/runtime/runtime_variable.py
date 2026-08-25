from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(slots=True)
class RuntimeVariable:

    id: str

    name: str

    data_type: str

    expression: str = None

    # Raw value received directly from driver
    value: object = None

    # Value after converter / expression
    cooked_value: object = None

    message: str | None = None

    quality: str = "Unknown"

    timestamp: datetime | None = None