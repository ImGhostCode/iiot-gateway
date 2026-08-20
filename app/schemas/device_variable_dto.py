from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.base import (
    DataTypeEnum,
    EndianEnum,
    ProtectTypeEnum,
)


class DeviceVariableBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    method: str = Field(..., min_length=1, max_length=255)
    device_address: str = Field(..., min_length=1, max_length=255)
    data_type: DataTypeEnum = (DataTypeEnum.Default)
    is_trigger: bool = False
    endian_type: EndianEnum = EndianEnum.None_
    expressions: Optional[str] = None
    is_upload: bool = True
    protect_type: ProtectTypeEnum = ProtectTypeEnum.ReadWrite
    index: int = Field(0, ge=0)
    alias: Optional[str] = Field(None, max_length=255)


class DeviceVariableCreate(DeviceVariableBase):
    pass


class DeviceVariableUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    method: Optional[str] = Field(None, min_length=1, max_length=255)
    device_address: Optional[str] = Field(None, min_length=1, max_length=255)
    data_type: Optional[DataTypeEnum] = None
    is_trigger: Optional[bool] = None
    endian_type: Optional[EndianEnum] = None
    expressions: Optional[str] = None
    is_upload: Optional[bool] = None
    protect_type: Optional[ProtectTypeEnum] = None
    index: Optional[int] = Field(None, ge=0)
    alias: Optional[str] = Field(None, max_length=255)


class DeviceVariableResponse(DeviceVariableBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    device_id: Optional[UUID] = None
    value: Optional[Any] = None
    cooked_value: Optional[Any] = None
    message: Optional[str] = None
    quality: Optional[str] = None
    timestamp: Optional[datetime] = None


class DeviceVariableWriteRequest(BaseModel):
    value: Any


class DeviceVariableWriteResponse(BaseModel):
    id: UUID
    device_id: UUID
    name: str
    requested_value: Any
    success: bool
    message: str


class DeviceVariableRuntimeResponse(BaseModel):
    id: UUID
    device_id: UUID
    name: str
    value: Any = None
    quality: str
    timestamp: Optional[datetime] = None
