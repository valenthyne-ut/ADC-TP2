from abc import ABC
from sqlite3 import Connection

class BaseSchema(ABC):
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