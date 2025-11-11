from abc import ABC, abstractmethod
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Any, Generic, Literal

from app.database.models.Base import T

@dataclass
class Filter:
    name: str
    value: Any
    comparison_operator: Literal["=", "<>", "!=", "<", "<=", ">=", ">", "LIKE"] = "="
    logical_operator: Literal["AND", "OR", "NOT"] = "AND"

class BaseSchema(ABC, Generic[T]):
    def __init__(self, connection: Connection):
        self._connection = connection

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

    @staticmethod
    def _construct_basic_filter_clause(filters: list[Filter]) -> tuple[str, dict[str, Any]]:
        if len(filters) <= 0:
            raise ValueError("O argumento 'filters' tem de ter pelo menos um valor!")
        
        clause = ""
        params: dict[str, Any] = {}

        for index, filter in enumerate(filters):
            if filter.value is not None:
                lop = filter.logical_operator if index > 0 else ""
                name = filter.name
                value = filter.value
                cop = filter.comparison_operator

                clause = f"{clause} {lop} {name} {cop} :{name}"
                if cop == "LIKE" and isinstance(value, str):
                    value = f"%{value}%"

                params[name] = value

        return clause, params

    @abstractmethod
    def find_one(self) -> T | None:
        ...

    @abstractmethod
    def find_many(self, limit: int = 2000) -> list[T]:
        ...

    @abstractmethod
    def create_one(self) -> T:
        ...

    @abstractmethod
    def delete(self, instance: T) -> bool:
        ...