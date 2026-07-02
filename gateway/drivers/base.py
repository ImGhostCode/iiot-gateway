from abc import ABC, abstractmethod
from collections.abc import Callable

from gateway.core.datapoint import DataPoint

DataCallback = Callable[[DataPoint], None]

class BaseDriver(ABC):
    def __init__(self, on_data: DataCallback):
        self._on_data = on_data

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError
    
    def emit(self, point: DataPoint) -> None:
        self._on_data(point)