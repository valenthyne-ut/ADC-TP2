from sqlite3 import Connection

from app.database.models.User import User
from app.database.schema.BaseSchema import BaseSchema, Filter

class UserSchema(BaseSchema["User"]):
    instance: "UserSchema"

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
        UserSchema.instance = self

    def find_one(self, id: int | None = None, alias: str | None = None, full_name: str | None = None) -> User | None:
        """
        Pesquisa por um utilizador do sistema na base de dados. Pelo menos um dos
        parâmetros tem de ser especificado.

        :param id: O ID único do utilizador.
        :param alias: O "nome de utilizador".
        :param full_name: O nome completo do utilizador.
        :type id: int
        :type alias: str
        :type full_name: str
        :return: O utilizador do sistema, se um foi encontrado.
        :rtype: User | None
        :raises ValueError: Se nenhum dos parâmetros foi especificado.
        """
        if id is None and alias is None and full_name is None:
            raise ValueError("Um parâmetro dos 'id', 'alias' ou 'name' tem de ser especificado!")
        
        base_query = """
            SELECT id, alias, full_name
            FROM User
        """

        query = base_query

        clause, params = BaseSchema._construct_basic_filter_clause([
            Filter("alias", alias, "LIKE"),
            Filter("full_name", full_name, "LIKE"),
        ])

        if len(clause) > 0:
            query = f"{query} WHERE {clause} LIMIT 1"
        
        if id is not None:
            query = f"{base_query} WHERE id=:id"
            params.clear()
            params["id"] = id 

        cursor = self._connection.cursor()
        result = cursor.execute(query, params).fetchone()

        return User(result[0], result[1], result[2])


    def find_many(self, limit: int = 2000, alias: str | None = None, name: str | None = None) -> list[User]:
        """
        Pesquisa por vários utilizadores do sistema.

        :param limit: O número máximo de resultados a devolver.
        :param alias: O "nome de utilizador".
        :param name: O nome completo do utilizador.
        :type limit: int = 2000
        :type alias: str
        :type name: str
        :return: Uma lista de utilizadores do sistema, se algum foi encontrado.
        :rtype: list[User]
        """
        cursor = self._connection.cursor()

        base_query = """
            SELECT id, alias, full_name
            FROM User
        """

        query = base_query

        clause, params = BaseSchema._construct_basic_filter_clause([
            Filter("alias", alias, "LIKE"),
            Filter("full_name", name, "LIKE")
        ])

        if len(clause) > 0:
            query = f"{query} WHERE {clause}"
            
        query = f"{query} LIMIT :limit"
        params["limit"] = limit

        result = cursor.execute(query, params).fetchall()

        user_list: list[User] = []
        
        for item in result:
            user_list.append(User(item[0], item[1], item[2]))

        return user_list

    def create_one(self, alias: str = "Unspecified", full_name: str = "Unspecified") -> User:
        """
        Insere um utilizador do sistema na base de dados e devolve o mesmo. Nenhum
        dos parâmetros são obrigatórios, sendo por defeito ``"Unspecified"``.

        :param alias: O "nome do utilizador".
        :param full_name: O nome completo do utilizador.
        :type alias: str
        :type full_name: str
        :return: O utilizador do sistema criado.
        :rtype: User
        :raises ValueError: Se algo correu mal ao inserir o utilizador do sistema na base de dados.
        """
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
        """
        Apaga um utilizador do sistema da base de dados.

        :param instance: Uma instância de um utilizador de sistema.
        :type instance: User
        :return: Um booleano que representa se foi ou não apagado o utilizador da base de dados.
        :rtype: bool
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            DELETE FROM User
            WHERE id=:id
        """, {
            "id": instance.id
        })

        return cursor.rowcount > 0