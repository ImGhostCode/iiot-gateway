from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(slots=True)
class TagChangedEvent:

    device_id: str

    variable_id: str

    old_value: object

    new_value: object
    
    timestamp: datetime