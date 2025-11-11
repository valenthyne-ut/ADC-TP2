from sqlite3 import Connection

from app.database.models.Technician import Technician
from app.database.schema.BaseSchema import BaseSchema

class TechnicianSchema(BaseSchema["Technician"]):
    instance: "TechnicianSchema"

    def __init__(self, connection: Connection):
        super().__init__(connection)
        if not self._table_exists("Technician"):
            if not self._table_exists("User"):
                raise LookupError("Tabela de User não existe, sendo a Technician dependente dela. Tente reiniciar a base de dados.")

            if not self._table_exists("ContactInfo"):
                raise LookupError("Tabela de ContactInfo não existe, sendo a Technician dependente dela. Tente reinicar a base de dados.")

            if not self._table_exists("Service"):
                raise LookupError("Tabela de Service não existe, sendo a Technician dependente dela. Tente reinicar a base de dados.")

            cursor = self._connection.cursor()
            cursor.execute("""
                CREATE TABLE Technician(
                    id INTEGER NOT NULL PRIMARY KEY,
                    contact_id INTEGER NOT NULL,
                    specialization_id INTEGER NOT NULL,
                    FOREIGN KEY(id) REFERENCES User(id),
                    FOREIGN KEY(contact_id) REFERENCES ContactInfo(id),
                    FOREIGN KEY(specialization_id) REFERENCES Service(id)
                )
            """)
        TechnicianSchema.instance = self

    def find_one(self, user_id: int | None = None) -> Technician | None:
        if user_id is None:
            raise ValueError("Parâmetro 'user_id' tem de ser especificado!")

        query = """
            SELECT id, contact_id, specialization_id
            FROM Technician
            WHERE id=:id
        """

        cursor = self._connection.cursor()
        result = cursor.execute(query, {
            "id": user_id
        }).fetchone()

        return Technician(result[0], result[1], result[2])

    def find_many(self, limit: int = 2000) -> list[Technician]:
        cursor = self._connection.cursor()

        query = """
            SELECT id, contact_id, specialization_id
            FROM Technician
            LIMIT :limit
        """

        result = cursor.execute(query, {
            "limit": limit
        }).fetchall()

        technician_list: list[Technician] = []

        for item in result:
            technician_list.append(Technician(item[0], item[1], item[2]))

        return technician_list

    def create_one(self, user_id: int | None = None, contact_id: int | None = None, specialization_id: int | None = None) -> Technician:
        if user_id is None or contact_id is None or specialization_id is None:
            raise ValueError("Todos os parâmetros 'user_id', 'contact_id' e 'specialization_id' têm de ser especificados!")

        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO Technician(id, contact_id, specialization_id)
            VALUES(:id, :contact_id, :specialization_id)
        """, {
            "id": user_id,
            "contact_id": contact_id,
            "specialization_id": specialization_id
        })

        if cursor.lastrowid is None:
            raise ValueError("Algo correu mal ao inserir os dados!")

        return Technician(cursor.lastrowid, contact_id, specialization_id)

    def delete(self, instance: Technician) -> bool:
        cursor = self._connection.cursor()
        cursor.execute("""
            DELETE FROM Technician
            WHERE id=:id
        """, {
            "id": instance.id
        })

        return cursor.rowcount > 0