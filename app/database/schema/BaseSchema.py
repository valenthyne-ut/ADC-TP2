from abc import ABC, abstractmethod
from dataclasses import field
from sqlite3 import Connection
from typing import Generic, Self

from app.database.models.Base import T

class BaseSchema(ABC, Generic[T]):
    instance: Self = field(init=False)

    def __init__(self, connection: Connection):
        self._connection = connection
        BaseSchema.instance = self

    def _table_exists(self, table_name: str) -> bool:
        cursor = self._connection.cursor()
        result = cursor.execute("""
            SELECT name 
            FROM sqlite_master
            WHERE type='table' AND name=:name
        """, {
            "name": table_name
        }).fetchall()

        return len(result) > 0

    @abstractmethod
    def find_one(self) -> T | None:
        ...

    @abstractmethod
    def find_many(self) -> list[T]:
        ...

    @abstractmethod
    def create_one(self) -> T:
        ...

    @abstractmethod
    def delete(self, instance: T) -> None:
        ...