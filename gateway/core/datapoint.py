
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass
class DataPoint:
    device_id: str
    measurement: str
    value: float
    protocol: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: dict[str, Any] = field(default_factory=dict)

    def to_influx_dict(self) -> dict:
        return {
            "measurement": self.measurement,
            "tags": {
                "device_id": self.device_id,
                "protocol": self.protocol,
                **self.tags,
            },
            "fields": {"value": self.value},
            "time": self.timestamp
        }