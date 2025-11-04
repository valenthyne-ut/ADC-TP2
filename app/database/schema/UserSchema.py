from sqlite3 import Connection

from app.database.models.User import User
from app.database.schema.BaseSchema import BaseSchema

class UserSchema(BaseSchema["User"]):
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

    def find_one(self, id: int | None = None, like_name: str | None = None) -> User | None:
        if id is None and like_name is None:
            raise ValueError("Um parâmetro de 'id' e 'like_name' tem de ser especificado!")
        
        cursor = self._connection.cursor()
        
        if id is not None:
            result = cursor.execute("""
                SELECT id, name
                FROM User
                WHERE id=:id
            """, {
                "id": id
            }).fetchone()
        else:
            result = cursor.execute("""
                SELECT id, name
                FROM User
                WHERE name LIKE :name
                LIMIT 1
            """, {
                "name": like_name
            }).fetchone()

        if result is not None:
            return User(result[0], result[1])

    def find_many(self, limit: int = 2000, like_name: str | None = None) -> list[User]:
        cursor = self._connection.cursor()

        if like_name is None:
            result = cursor.execute("""
                SELECT id, name
                FROM User
                LIMIT :limit
            """, {
                "limit": limit
            }).fetchall()
        else:
            result = cursor.execute("""
                SELECT id, name
                FROM User
                WHERE name LIKE :name
                LIMIT :limit
            """, {
                "name": like_name,
                "limit": limit
            }).fetchall()

        user_list: list[User] = []
        
        for item in result:
            user_list.append(User(item[0], item[1]))

        return user_list

    def create_one(self, name: str = "Unspecified") -> User:
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO User(name)
            VALUES(:name)
        """, {
            "name": name
        })

        if cursor.lastrowid is None:
            raise ValueError("Algo correu mal ao inserir os dados!")

        return User(cursor.lastrowid, name)
        
    def delete(self, instance: User) -> None:
        return None