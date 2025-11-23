from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T", bound="Base", default="Base")

@dataclass
class Base(ABC, Generic[T]):
    id: int
    """
    O identificator único do conjunto de dados. Presente em todas
    as subclasses "model" da base de dados.
    """

    @abstractmethod
    def __str__(self) -> str:
        return f"{id}"