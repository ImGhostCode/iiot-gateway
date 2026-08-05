import uuid
from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import (
    Enum as SqlEnum,
    ForeignKey,
    String,
    DateTime

)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.base import BasePoco, DataSide


class DeviceConfig(BasePoco):
    __tablename__ = "device_configs"

    device_config_name: Mapped[str] = mapped_column(String, index=True, comment="Name")
    data_side: Mapped[DataSide] = mapped_column(SqlEnum(DataSide), comment="Attribute side")
    description: Mapped[str] = mapped_column(String, comment="Description")
    value: Mapped[str] = mapped_column(String, index=True, comment="Value")
    enum_info: Mapped[str] = mapped_column(String, comment="Remark")

    create_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc))
    create_by: Mapped[Optional[str]] = mapped_column(String(50))
    update_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),)
    update_by: Mapped[Optional[str]] = mapped_column(String(50))

    device_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("devices.id"), comment="Equipment")
    device: Mapped[Optional["Device"]] = relationship(back_populates="device_configs")
