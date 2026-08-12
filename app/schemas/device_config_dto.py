from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.base import DataSide


class DeviceConfigBase(BaseModel):
    device_config_name: str = Field(..., min_length=1, max_length=255)
    data_side: DataSide = DataSide.AnySide
    description: Optional[str] = None
    value: Optional[str] = Field(None, max_length=255)
    enum_info: Optional[str] = None


class DeviceConfigCreate(DeviceConfigBase):
    pass


class DeviceConfigUpdate(BaseModel):
    device_config_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
    )

    data_side: Optional[DataSide] = None

    description: Optional[str] = None

    value: Optional[str] = Field(
        None,
        max_length=255,
    )

    enum_info: Optional[str] = None


class DeviceConfigResponse(DeviceConfigBase):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID

    device_id: uuid.UUID

    create_time: Optional[datetime] = None
    create_by: Optional[str] = None

    update_time: Optional[datetime] = None
    update_by: Optional[str] = None


class DeviceConfigSchemaItem(BaseModel):

    name: str

    description: Optional[str] = None

    default: Optional[str] = None

    data_side: DataSide = DataSide.AnySide

    enum_info: Optional[str] = None


class DeviceConfigSchemaResponse(BaseModel):

    device_id: uuid.UUID

    driver: Optional[str] = None

    configs: list[DeviceConfigSchemaItem]