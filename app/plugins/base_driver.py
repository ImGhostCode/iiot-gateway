from abc import ABC
from abc import abstractmethod

class BaseDriver(ABC):

    def __init__(self, device):
        self.device = device

    @abstractmethod
    async def connect(self):
        """Connect to device."""

    @abstractmethod
    async def disconnect(self):
        """Disconnect from device."""

    @abstractmethod
    async def read(self):
        """Read all variables."""

    @abstractmethod
    async def write(self, variable, value):
        """Write one variable."""