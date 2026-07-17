from dataclasses import dataclass


@dataclass(slots=True)
class RawValue:

    variable_id: int

    value: object