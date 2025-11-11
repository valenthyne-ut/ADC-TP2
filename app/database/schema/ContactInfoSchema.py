from sqlite3 import Connection
from app.database.schema import BaseSchema

from app.database.models.ContactInfo import ContactInfo
from app.database.schema.BaseSchema import BaseSchema, Filter

class ContactInfoSchema(BaseSchema["ContactInfo"]):
    def __init__(self, connection: Connection):
        super().__init__(connection)
        if not self._table_exists("ContactInfo"):
            cursor = self._connection.cursor()
            cursor.execute("""
                CREATE TABLE ContactInfo(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(255) NOT NULL,
                    phone_num VARCHAR(15) NOT NULL,
                    address VARCHAR(255)
                );
            """)

    def find_one(self, id: int | None = None, email: str | None = None, phone_num: str | None = None, address: str | None = None) -> ContactInfo | None:
        if id is None and email is None and phone_num is None and address is None:
            raise ValueError("Um parâmetro dos 'id', 'email', 'phone_num' ou 'address' tem de ser especificado!")

        base_query = """
            SELECT id, email, phone_num, address
            FROM ContactInfo
        """

        query = base_query

        clause, params = BaseSchema._construct_basic_filter_clause([
            Filter("email", email, "LIKE"),
            Filter("phone_num", phone_num, "LIKE"),
            Filter("address", address, "LIKE")
        ])

        if len(clause) > 0:
            query = f"{query} WHERE {clause} LIMIT 1"

        if id is not None:
            query = f"{base_query} WHERE id=:id"
            params.clear()
            params["id"] = id

        cursor = self._connection.cursor()
        result = cursor.execute(query, params).fetchone()

        return ContactInfo(result[0], result[1], result[2], result[3])

    def find_many(self, limit: int = 2000, email: str | None = None, phone_num: str | None = None, address: str | None = None) -> list[ContactInfo]:
        cursor = self._connection.cursor()

        base_query = """
            SELECT id, email, phone_num, address
            FROM ContactInfo
        """

        query = base_query

        clause, params = BaseSchema._construct_basic_filter_clause([
            Filter("email", email, "LIKE"),
            Filter("phone_num", phone_num, "LIKE"),
            Filter("address", address, "LIKE")
        ])

        if len(clause) > 0:
            query = f"{query} WHERE {clause} LIMIT 1"

        query = f"{query} LIMIT :limit"
        params["limit"] = limit

        result = cursor.execute(query, params).fetchall()

        contactinfo_list: list[ContactInfo] = []
        
        for item in result:
            contactinfo_list.append(ContactInfo(item[0], item[1], item[2], item[3]))

        return contactinfo_list

    def create_one(self, email: str = "Unspecified", phone_num: str = "+00000000000000", address: str = "Unspecified") -> ContactInfo:
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO ContactInfo(email, phone_num, address)
            VALUES(:email, :phone_num, :address)
        """, {
            "email": email,
            "phone_num": phone_num,
            "address": address
        })

        if cursor.lastrowid is None:
            raise ValueError("Algo correu mal ao inserir os dados!")

        return ContactInfo(cursor.lastrowid, email, phone_num, address)
    
    def delete(self, instance: ContactInfo) -> bool:
        cursor = self._connection.cursor()
        cursor.execute("""
            DELETE FROM ContactInfo
            WHERE id=:id
        """, {
            "id": instance.id
        })

        return cursor.rowcount > 0