from dataclasses import dataclass


@dataclass(slots=True)
class RawValue:

    variable_id: str

    value: object