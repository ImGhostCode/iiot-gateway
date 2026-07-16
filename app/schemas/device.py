from pydantic import BaseModel

class DeviceCreate(BaseModel):
    name: str
    protocol: str
    ip: str
    port:int
    polling_interval: int = 1000