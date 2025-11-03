from abc import ABC
from sqlite3 import Connection
from typing import Self
from dataclasses import field

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