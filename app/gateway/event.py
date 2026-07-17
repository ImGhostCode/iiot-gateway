from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(slots=True)
class TagChangedEvent:

    device_id: int

    variable_id: int

    old_value: object

    new_value: object
    
    timestamp: datetime