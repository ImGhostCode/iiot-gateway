from abc import ABC
from abc import abstractmethod

from app.db.models.device import Device
from app.gateway.runtime.raw_value import RawValue

class BaseDriver(ABC):

    def __init__(self, device: Device):
        self.device = device
        self.runtime = None
        self.connected = False

    @abstractmethod
    async def connect(self):
        """Connect to device."""

    @abstractmethod
    async def disconnect(self):
        """Disconnect from device."""   

    @abstractmethod
    async def read(self) -> list[RawValue]:
        """Read all variables."""

    @abstractmethod
    async def write(self, variable, value):
        """Write one variable."""

    @abstractmethod
    async def initialize(self):
        """Called after configs are loaded."""
        pass