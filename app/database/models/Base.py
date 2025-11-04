from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T", bound="Base", default="Base")

@dataclass
class Base(ABC, Generic[T]):
    id: int

    @abstractmethod
    def __str__(self) -> str:
        return f"{id}"