import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import (
    BasePoco,
    DataTypeEnum,
    EndianEnum,
    ProtectTypeEnum,
)


class DeviceVariable(BasePoco):
    __tablename__ = "device_variables"

    name: Mapped[str] = mapped_column(String, index=True, comment="Variable name")
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True, comment="Description")
    method: Mapped[str] = mapped_column(String, index=True, comment="Method")
    device_address: Mapped[str] = mapped_column(String, index=True, comment="Address")
    data_type: Mapped[DataTypeEnum] = mapped_column(SqlEnum(DataTypeEnum), index=True, comment="Data types")
    is_trigger: Mapped[bool] = mapped_column(Boolean, default=False, comment="Trigger")
    endian_type: Mapped[EndianEnum] = mapped_column(SqlEnum(EndianEnum), comment="Endian")
    expressions: Mapped[Optional[str]] = mapped_column(String, nullable=True, comment="Expression")
    is_upload: Mapped[bool] = mapped_column(Boolean, default=True, comment="Upload")
    protect_type: Mapped[ProtectTypeEnum] = mapped_column(SqlEnum(ProtectTypeEnum), comment="Permissions")
    index: Mapped[int] = mapped_column(Integer, default=0, comment="Sort")
    alias: Mapped[Optional[str]] = mapped_column(String, nullable=True, comment="Alias")

    device_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("devices.id"), nullable=True, comment="Device")
    device: Mapped[Optional["Device"]] = relationship(back_populates="device_variables")

    @property
    def value(self):
        return getattr(self, "_value", None)

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def cooked_value(self):
        return getattr(self, "_cooked_value", None)

    @cooked_value.setter
    def cooked_value(self, val):
        self._cooked_value = val

    @property
    def message(self):
        return getattr(self, "_message", None)

    @message.setter
    def message(self, val):
        self._message = val

    @property
    def quality(self):
        return getattr(self, "_quality", "Unknown")

    @quality.setter
    def quality(self, val):
        self._quality = val

    @property
    def timestamp(self):
        return getattr(self, "_timestamp", None)

    @timestamp.setter
    def timestamp(self, val):
        self._timestamp = val
