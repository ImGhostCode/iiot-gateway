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
    Group = 0
    Device = 1

class AccessEnum(int, Enum):
    ReadOnly = 0
    ReadAndWrite = 1

class DataSide(int, Enum):
    AnySide = 0
    ClientSide = 2

# Placeholders for enums referenced but not fully defined in the provided code
class ProtectTypeEnum(str, Enum):
    ReadOnly = "ReadOnly"
    ReadWrite = "ReadWrite"
    WriteOnly = "WriteOnly"


class DataTypeEnum(str, Enum):
    Bit = "Bit"
    Bool = "Bool"
    UByte = "UByte"
    Byte = "Byte"
    Uint16 = "Uint16"
    Int16 = "Int16"
    Bcd16 = "Bcd16"
    Uint32 = "Uint32"
    Int32 = "Int32"
    Float = "Float"
    Bcd32 = "Bcd32"
    Uint64 = "Uint64"
    Int64 = "Int64"
    Double = "Double"
    AsciiString = "AsciiString"
    Utf8String = "Utf8String"
    DateTime = "DateTime"
    TimeStampMs = "TimeStampMs"
    TimeStampS = "TimeStampS"
    Any = "Any"
    Custome1 = "Custome1"
    Custome2 = "Custome2"
    Custome3 = "Custome3"
    Custome4 = "Custome4"
    Custome5 = "Custome5"
    Gb2312String = "Gb2312String"
    Default = "Default"


class EndianEnum(str, Enum):
    None_ = "None"
    BigEndian = "BigEndian"
    LittleEndian = "LittleEndian"
    BigEndianSwap = "BigEndianSwap"
    LittleEndianSwap = "LittleEndianSwap"


class VaribaleStatusTypeEnum(str, Enum):
    Good = "Good"
    AddressError = "AddressError"
    MethodError = "MethodError"
    ExpressionError = "ExpressionError"
    Bad = "Bad"
    UnKnow = "UnKnow"
    Custome1 = "Custome1"
    Custome2 = "Custome2"
    Custome3 = "Custome3"
    Custome4 = "Custome4"
    Custome5 = "Custome5"

class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"

class Base(DeclarativeBase):
    pass

class BasePoco(Base):
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

class BaseEntity:

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )