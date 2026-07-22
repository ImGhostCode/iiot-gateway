from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class DriverCreate(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    driver_name: str = Field(..., min_length=1, max_length=100)

    file_name: str = Field(..., min_length=1, max_length=200)

    assemble_name: str = Field(..., min_length=1, max_length=200)

    authorize_num: int = Field(..., ge=0)
