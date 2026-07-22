import uuid
from typing import Optional

from sqlalchemy import (
    Enum as SqlEnum,
    ForeignKey,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BasePoco, DataSide
from app.db.models.device import Device


class DeviceConfig(BasePoco):
    __tablename__ = "device_configs"

    device_config_name: Mapped[str] = mapped_column(String, index=True, comment="Name")
    data_side: Mapped[DataSide] = mapped_column(SqlEnum(DataSide), comment="Attribute side")
    description: Mapped[str] = mapped_column(String, comment="Description")
    value: Mapped[str] = mapped_column(String, index=True, comment="Value")
    enum_info: Mapped[str] = mapped_column(String, comment="Remark")

    device_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("devices.id"), comment="Equipment")
    device: Mapped[Optional["Device"]] = relationship(back_populates="device_configs")
