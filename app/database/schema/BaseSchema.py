from abc import ABC, abstractmethod
from sqlite3 import Connection
from typing import Self
from dataclasses import field
from app.database.models.Base import Base

class BaseSchema(ABC):
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
    def find_one(self) -> Base | None:
        ...

    @abstractmethod
    def find_many(self) -> list[Base]:
        ...

    @abstractmethod
    def create_one(self) -> Base:
        ...

    @abstractmethod
    def delete(self, instance: Base) -> None:
        ...