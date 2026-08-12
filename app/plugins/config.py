from dataclasses import dataclass
from typing import Optional

from app.db.models.base import DataSide


@dataclass(slots=True)
class ConfigParameter:

    name: str

    description: Optional[str] = None

    default: Optional[str] = None

    data_side: DataSide = DataSide.AnySide

    enum_info: Optional[str] = None