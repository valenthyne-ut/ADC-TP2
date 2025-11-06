from sqlite3 import Connection
from typing import Any

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
                    alias VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255) NOT NULL
                );
            """)

    def find_one(self, id: int | None = None, like_alias: str | None = None, like_name: str | None = None) -> User | None:
        if id is None and like_alias is None and like_name is None:
            raise ValueError("Um parâmetro de 'id', 'like_alias' ou 'like_name' tem de ser especificado!")
        
        query = """
            SELECT id, alias, full_name
            FROM User
        """

        filters: list[str] = []
        params: dict[str, Any] = {}

        cursor = self._connection.cursor()
        
        if like_alias is not None:
            filters.append("alias = :alias")
            params["alias"] = like_alias
        
        if like_name is not None:
            filters.append("full_name = :name")
            params["name"] = like_name
        
        if id is not None:
            filters.clear()
            params.clear()

            filters.append("id = :id")
            params["id"] = id

        if len(filters) > 0:
            query = f"{query} WHERE {' AND '.join(filters)} LIMIT 1"
        else:
            query = f"{query} LIMIT 1"
        
        result = cursor.execute(query, params).fetchone()

        return User(result[0], result[1], result[2])


    def find_many(self, limit: int = 2000, like_alias: str | None = None, like_name: str | None = None) -> list[User]:
        cursor = self._connection.cursor()

        query = """
            SELECT id, alias, full_name
            FROM User
        """

        filters: list[str] = []
        params: dict[str, Any] = {}

        cursor = self._connection.cursor()
        
        if like_alias is not None:
            filters.append("alias = :alias")
            params["alias"] = like_alias
        
        if like_name is not None:
            filters.append("full_name = :name")
            params["name"] = like_name

        if len(filters) > 0:
            query = f"{query} WHERE {' AND '.join(filters)} LIMIT :limit"
        else:
            query = f"{query} LIMIT :limit"

        params["limit"] = limit

        result = cursor.execute(query, params).fetchall()

        user_list: list[User] = []
        
        for item in result:
            user_list.append(User(item[0], item[1], item[2]))

        return user_list

    def create_one(self, alias: str = "Unspecified", full_name: str = "Unspecified") -> User:
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO User(alias, full_name)
            VALUES(:alias, :name)
        """, {
            "alias": alias,
            "name": full_name
        })

        if cursor.lastrowid is None:
            raise ValueError("Algo correu mal ao inserir os dados!")

        return User(cursor.lastrowid, alias, full_name)
        
    def delete(self, instance: User) -> bool:
        cursor = self._connection.cursor()
        cursor.execute("""
            DELETE FROM User
            WHERE id=:id
        """, {
            "id": instance.id
        })

        return cursor.rowcount > 0