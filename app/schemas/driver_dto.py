from datetime import datetime
from typing import Any, Optional

import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class DriverBase(BaseModel):

    driver_name: Optional[str] = None

    file_name: Optional[str] = None

    assemble_name: Optional[str] = None

    authorizes_num: int = Field(
        default=0,
        ge=0,
    )


class DriverCreate(BaseModel):

    file_name: str = Field(
        min_length=1,
        max_length=255,
    )

    authorizes_num: int = Field(
        default=0,
        ge=0,
    )


class DriverUpdate(BaseModel):

    file_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
    )

    authorizes_num: Optional[int] = Field(
        None,
        ge=0,
    )


class DriverResponse(DriverBase):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID

    create_time: Optional[datetime] = None

    create_by: Optional[str] = Field(
        None,
        max_length=50,
    )

    update_time: Optional[datetime] = None

    update_by: Optional[str] = Field(
        None,
        max_length=50,
    )


class PluginConfigParameterResponse(
    BaseModel
):

    name: str

    description: str

    data_type: str

    default: Any = None

    required: bool

    enum_values: dict[str, Any] = Field(
        default_factory=dict
    )


class DiscoveredPluginResponse(
    BaseModel
):

    name: str

    version: str

    author: str

    description: str

    driver: str

    config_parameters: list[
        PluginConfigParameterResponse
    ] = Field(
        default_factory=list
    )


class PluginAvailableResponse(
    DiscoveredPluginResponse
):

    registered: bool

    driver_id: Optional[uuid.UUID] = None