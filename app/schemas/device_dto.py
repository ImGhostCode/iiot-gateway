from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.db.models.base import (
    DeviceTypeEnum,
)

from app.schemas.device_config_dto import (
    DeviceConfigResponse,
)

from app.schemas.device_variable_dto import (
    DeviceVariableResponse,
)


class DeviceBase(BaseModel):

    device_name: str = Field(
        min_length=1,
        max_length=255,
    )

    index: int = Field(
        default=0,
        ge=0,
    )

    description: str = ""

    driver_id: Optional[UUID] = None

    auto_start: bool = True

    cg_upload: bool = True

    enforce_period: int = Field(
        default=1000,
        ge=100,
    )

    cmd_period: int = Field(
        default=100,
        ge=0,
    )

    device_type_enum: DeviceTypeEnum = (
        DeviceTypeEnum.Device
    )

    parent_id: Optional[UUID] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):

    device_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
    )

    index: Optional[int] = Field(
        None,
        ge=0,
    )

    description: Optional[str] = None

    driver_id: Optional[UUID] = None

    auto_start: Optional[bool] = None

    cg_upload: Optional[bool] = None

    enforce_period: Optional[int] = Field(
        None,
        ge=100,
    )

    cmd_period: Optional[int] = Field(
        None,
        ge=0,
    )

    device_type_enum: Optional[
        DeviceTypeEnum
    ] = None

    parent_id: Optional[UUID] = None


class DeviceResponse(DeviceBase):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID

    create_time: Optional[datetime] = None

    create_by: Optional[str] = None

    update_time: Optional[datetime] = None

    update_by: Optional[str] = None

    device_configs: list[
        DeviceConfigResponse
    ] = Field(
        default_factory=list
    )

    device_variables: list[
        DeviceVariableResponse
    ] = Field(
        default_factory=list
    )


class DeviceRuntimeStatusResponse(
    BaseModel
):

    id: UUID

    device_name: str

    connected: bool

    polling: bool

    read_count: int

    error_count: int

    reconnect_count: int

    last_poll: Optional[datetime]

    last_error: Optional[str]


class DeviceVariableRuntimeResponse(
    BaseModel
):

    id: UUID

    name: str

    value: object = None

    quality: str

    timestamp: Optional[datetime]