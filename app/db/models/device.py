import uuid
from typing import List, Optional
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BasePoco, DeviceTypeEnum
from app.db.models.device_config import DeviceConfig
from app.db.models.device_variable import DeviceVariable

class Device(BasePoco):
    __tablename__ = "devices"

    device_name: Mapped[str] = mapped_column(String, index=True, comment="Device name")
    index: Mapped[int] = mapped_column(Integer, comment="Sort")
    description: Mapped[str] = mapped_column(String, comment="Description")
    
    driver_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("drivers.id"), comment="Driver")
    # from app.db.models.driver import Driver 
    driver: Mapped[Optional["Driver"]] = relationship(back_populates="devices")

    # auto_start == true -> start polling when loaded driver
    auto_start: Mapped[bool] = mapped_column(Boolean, index=True, comment="Auto start up polling")
    # cg_upload == true -> always upload
    # cg_upload == false -> time is exceccded or value is changed -> upload
    cg_upload: Mapped[bool] = mapped_column(Boolean, comment="Changes uploaded")
    enforce_period: Mapped[int] = mapped_column(Integer, comment="Polling cycle ms")
    cmd_period: Mapped[int] = mapped_column(Integer, comment="Instruction interval ms") # Delay between variable readings
    device_type_enum: Mapped[DeviceTypeEnum] = mapped_column(
        SqlEnum(DeviceTypeEnum), index=True, comment="Type (group or device)"
    )

    create_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc))
    create_by: Mapped[Optional[str]] = mapped_column(String(50))
    update_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),)
    update_by: Mapped[Optional[str]] = mapped_column(String(50))

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("devices.id"))
    children: Mapped[List["Device"]] = relationship(back_populates="parent")
    parent: Mapped[Optional["Device"]] = relationship(back_populates="children", remote_side="Device.id")

    # Relationships
    device_configs: Mapped[List["DeviceConfig"]] = relationship(back_populates="device", cascade="all, delete-orphan")
    device_variables: Mapped[List["DeviceVariable"]] = relationship(back_populates="device", cascade="all, delete-orphan")