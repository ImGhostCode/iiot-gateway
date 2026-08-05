from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from app.db.models.base import (
    IoTPlatformType,
)

class SystemConfigBase(BaseModel):
    gateway_name: Optional[str] = None
    client_id: Optional[str] = None
    mqtt_ip: Optional[str] = None
    mqtt_port: int
    mqtt_uname: Optional[str] = None
    mqtt_upwd: Optional[str] = None
    iot_platform_type: IoTPlatformType


class SystemConfigCreate(SystemConfigBase):
    pass


class SystemConfigUpdate(BaseModel):
    gateway_name: Optional[str] = None
    client_id: Optional[str] = None
    mqtt_ip: Optional[str] = None
    mqtt_port: Optional[int] = None
    mqtt_uname: Optional[str] = None
    mqtt_upwd: Optional[str] = None
    iot_platform_type: Optional[IoTPlatformType] = None


class SystemConfigResponse(SystemConfigBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    create_time: Optional[datetime] = None
    create_by: Optional[str] = Field(None, max_length=50)
    update_time: Optional[datetime] = None
    update_by: Optional[str] = Field(None, max_length=50)