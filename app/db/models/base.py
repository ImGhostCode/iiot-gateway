import uuid
from typing import List, Optional
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    Uuid
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

class IoTPlatformType(int, Enum):
    ThingsBoard = 0
    IoTSharp = 1
    AliCloudIoT = 2
    TencentIoTHub = 3
    BaiduIoTCore = 4
    OneNET = 5
    ThingsCloud = 6
    HuaWei = 7
    IoTGateway = 8
    ThingsPanel = 9

class DeviceTypeEnum(int, Enum):
    Group = 0 #[cite: 8]
    Device = 1 #[cite: 8]

class AccessEnum(int, Enum):
    ReadOnly = 0 #[cite: 8]
    ReadAndWrite = 1 #[cite: 8]

class DataSide(int, Enum):
    AnySide = 0 #[cite: 8]
    ClientSide = 2 #[cite: 8]

# Placeholders for enums referenced but not fully defined in the provided code
class ProtectTypeEnum(str, Enum):
    Default = "Default"

class DataTypeEnum(str, Enum):
    Default = "Default"

class EndianEnum(str, Enum):
    Default = "Default"

class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"

class Base(DeclarativeBase):
    pass

class BasePoco(Base):
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

class BaseEntity:

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )