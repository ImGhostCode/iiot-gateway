import uuid
from typing import Optional

from sqlalchemy import (
    Boolean,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BasePoco, DataTypeEnum, EndianEnum, ProtectTypeEnum
from app.db.models.device import Device

class DeviceVariable(BasePoco):
    __tablename__ = "device_variables"

    name: Mapped[str] = mapped_column(String, index=True, comment="Variable name")
    description: Mapped[str] = mapped_column(String, comment="Description")
    method: Mapped[str] = mapped_column(String, index=True, comment="Method")
    device_address: Mapped[str] = mapped_column(String, index=True, comment="Address")
    data_type: Mapped[DataTypeEnum] = mapped_column(SqlEnum(DataTypeEnum), index=True, comment="Data types")
    is_trigger: Mapped[bool] = mapped_column(Boolean, comment="Trigger")
    endian_type: Mapped[EndianEnum] = mapped_column(SqlEnum(EndianEnum), comment="Big-endian")
    expressions: Mapped[str] = mapped_column(String, comment="Expression")
    is_upload: Mapped[bool] = mapped_column(Boolean, comment="Upload")
    protect_type: Mapped[ProtectTypeEnum] = mapped_column(SqlEnum(ProtectTypeEnum), comment="Permissions")
    index: Mapped[int] = mapped_column(Integer, comment="Sort")
    alias: Mapped[str] = mapped_column(String, comment="Alias")

    device_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("devices.id"), comment="Equipment")
    device: Mapped[Optional["Device"]] = relationship(back_populates="device_variables")

    # Regular Python instance attributes
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