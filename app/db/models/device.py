from enum import Enum

from sqlalchemy import (
    Boolean, 
    Enum as SqlEnum,
    ForeignKey,
    String,
    Integer
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.models.base import BaseEntity

class DeviceTypeEnum(str, Enum):
    GROUP = "Group"
    DEVICE = "Device"

class Device(Base, BaseEntity):

    __tablename__ = "devices"

    device_name: Mapped[str] = mapped_column(String(100), index=True)

    index: Mapped[int] = mapped_column(Integer)

    description: Mapped[str | None]
    
    protocol: Mapped[str] = mapped_column(String(50))

    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))

    auto_start: Mapped[bool] = mapped_column(Boolean,default=True)

    cg_upload: Mapped[bool] = mapped_column(Boolean,default=True)

    enforce_period: Mapped[int] = mapped_column(Integer,default=1000)

    cmd_period: Mapped[int] = mapped_column(Integer,default=100)

    device_type: Mapped[DeviceTypeEnum] = mapped_column(SqlEnum(DeviceTypeEnum))

    driver = relationship(
        "Driver",
        back_populates="devices"
    )

    configs = relationship(
        "DeviceConfig",
        back_populates="device",
        cascade="all, delete-orphan"
    )

    variables = relationship(
        "DeviceVariable",
        back_populates="device",
        cascade="all, delete-orphan"
    )