from sqlalchemy import (
    ForeignKey, 
    String
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.models.base import BaseEntity

class DeviceVariable(Base, BaseEntity):

    __tablename__ = "device_variables"

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )

    name: Mapped[str] = mapped_column(String(100))
    
    address: Mapped[str] = mapped_column(String(50))

    data_type: Mapped[str] = mapped_column(String(30))

    value: Mapped[str | None]

    device = relationship(
        "Device",
        back_populates="variables",
    )