from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Base(ABC):
    id: int

    @abstractmethod
    def __str__(self) -> str:
        return f"{id}"