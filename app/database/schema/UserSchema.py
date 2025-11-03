from sqlite3 import Connection
from app.database.schema.BaseSchema import BaseSchema

class UserSchema(BaseSchema):
    def __init__(self, connection: Connection):
        super().__init__(connection)
        if not self._table_exists("User"):
            cursor = self._connection.cursor()
            cursor.execute("""
                CREATE TABLE User(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL
                );
            """)