from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class RuntimeVariable:

    id: int

    name: str

    value: object = None

    quality: str = "Good"

    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))