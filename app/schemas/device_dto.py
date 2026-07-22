from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from app.db.models.device import DeviceTypeEnum


class DeviceCreate(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    device_name: str = Field(..., min_length=1, max_length=100)
    index: int = Field(..., ge=0)

    description: Optional[str] = None
    
    protocol: str = Field(..., max_length=50)
    driver_id: int = Field(..., gt=0)

    auto_start: bool = True
    cg_upload: bool = True
    enforce_period: int = Field(1000, gt=0)
    cmd_period: int = Field(100, gt=0)

    device_type: DeviceTypeEnum