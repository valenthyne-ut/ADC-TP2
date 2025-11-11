from sqlite3 import Connection
from app.database.schema.BaseSchema import BaseSchema

from app.database.models.Client import Client

class ClientSchema(BaseSchema["Client"]):
    def __init__(self, connection: Connection):
        super().__init__(connection)
        if not self._table_exists("Client"):
            if not self._table_exists("User"):
                raise LookupError("Tabela de User não existe, sendo a Client dependente dela. Tente reiniciar a base de dados.")

            if not self._table_exists("ContactInfo"):
                raise LookupError("Tabela de ContactInfo não existe, sendo a Client dependente dela. Tente reinicar a base de dados.")

            cursor = self._connection.cursor()
            cursor.execute("""
                CREATE TABLE Client(
                    id INTEGER NOT NULL PRIMARY KEY,
                    contact_id INTEGER NOT NULL,
                    FOREIGN KEY(id) REFERENCES User(id),
                    FOREIGN KEY(contact_id) REFERENCES ContactInfo(id)
                )
            """)

    def find_one(self, user_id: int | None = None) -> Client | None:
        if user_id is None:
            raise ValueError("Parâmetro 'user_id' tem de ser especificado!")

        query = """
            SELECT id, contact_id
            FROM Client
            WHERE id=:id
        """

        cursor = self._connection.cursor()
        result = cursor.execute(query, {
            "id": user_id
        }).fetchone()

        return Client(result[0], result[1])

    def find_many(self, limit: int = 2000) -> list[Client]:
        cursor = self._connection.cursor()

        query = """
            SELECT id, contact_id
            FROM Client
            LIMIT :limit
        """

        result = cursor.execute(query, {
            "limit": limit
        }).fetchall()

        client_list: list[Client] = []

        for item in result:
            client_list.append(Client(item[0], item[1]))

        return client_list

    def create_one(self, user_id: int | None = None, contact_id: int | None = None) -> Client:
        if user_id is None or contact_id is None:
            raise ValueError("Ambos os parâmetros 'user_id' e 'contact_id' têm de ser especificados!")

        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO Client(id, contact_id)
            VALUES(:id, :contact_id)
        """, {
            "id": id,
            "contact_id": contact_id
        })

        if cursor.lastrowid is None:
            raise ValueError("Algo correu mal ao inserir os dados!")

        return Client(cursor.lastrowid, contact_id)

    def delete(self, instance: Client) -> bool:
        cursor = self._connection.cursor()
        cursor.execute("""
            DELETE FROM Client
            WHERE id=:id
        """, {
            "id": instance.id
        })

        return cursor.rowcount > 0