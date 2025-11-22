from sqlite3 import Connection
from app.database.models.Service import Service
from app.database.schema.BaseSchema import BaseSchema, Filter


class ServiceSchema(BaseSchema["Service"]):
    instance: "ServiceSchema"

    def __init__(self, connection: Connection):
        super().__init__(connection)
        if not self._table_exists("Service"):
            cursor = self._connection.cursor()
            cursor.execute("""
                CREATE TABLE Service(
                    id INTEGER NOT NULL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    duration_mins INTEGER NOT NULL
                )
            """)
        ServiceSchema.instance = self

    def find_one(self, id: int | None = None, name: str | None = None) -> Service | None:
        """
        Encontra um serviço na base de dados.
        Pelo menos um parâmetro tem de ser especificado.

        :param id: O ID único do serviço.
        :param name: O nome do serviço.
        :type id: int
        :type name: str
        :return: O serviço, se foi encontrado.
        :rtype: Service | None
        :raises ValueError: Se nenhum parâmetro foi especificado.
        """
        if id is None and name is None:
            raise ValueError("Um parâmetro dos 'id' ou 'name' tem de ser especificado!")
        
        base_query = """
            SELECT id, name, price, duration_mins
            FROM Service
        """

        query = base_query

        clause, params = BaseSchema._construct_basic_filter_clause([
            Filter("name", name, "LIKE")
        ])

        if len(clause) > 0:
            query = f"{query} WHERE {clause} LIMIT 1"

        if id is not None:
            query = f"{base_query} WHERE id=:id"
            params.clear()
            params["id"] = id

        cursor = self._connection.cursor()
        result = cursor.execute(query, params).fetchone()

        return Service(result[0], result[1], result[2], result[3])

    def find_many(self, limit: int = 2000, name: str | None = None) -> list[Service]:
        """
        Encontra vários serviços na base de dados.

        :param limit: O número máximo de resultados a devlover.
        :param name: O nome do serviço.
        :type limit: int
        :type name: str
        :return: Os serviços, se forem encontrados.
        :rtype: list[Service]
        """
        cursor = self._connection.cursor()

        base_query = """
            SELECT id, name, price, duration_mins
            FROM Service
        """

        query = base_query

        clause, params = BaseSchema._construct_basic_filter_clause([
            Filter("name", name, "LIKE")
        ])

        if len(clause) > 0:
            query = f"{query} WHERE {clause}"

        query = f"{query} LIMIT :limit"
        params["limit"] = limit

        result = cursor.execute(query, params).fetchall()

        service_list: list[Service] = []

        for item in result:
            service_list.append(Service(item[0], item[1], item[2], item[3]))

        return service_list

    def create_one(self, name: str = "Unspecified", price: float = -1, duration_mins: int = -1) -> Service:
        """
        Insere um serviço na base de dados e devolve esse mesmo. Todos
        os parâmetros são opcionais, sendo por defeito ``Unspecified``
        ou ``-1``.

        :param name: O nome do serviço a inserir.
        :param price: O preço do serviço a inserir.
        :param duration_mins: A duração do serviço (em minutos) a inserir.
        :type name: str
        :type price: float
        :type duration_mins: int
        :return: O serviço inserido.
        :rtype: Service
        :raises ValueError: Se algo correu mal ao inserir o serviço na base de dados.
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO Service(name, price, duration_mins)
            VALUES(:name, :price, :duration_mins)
        """, {
            "name": name,
            "price": price,
            "duration_mins": duration_mins
        })

        if cursor.lastrowid is None:
            raise ValueError("Algo correu mal ao inserir os dados!")

        return Service(cursor.lastrowid, name, price, duration_mins)

    def delete(self, instance: Service) -> bool:
        """
        Apaga um serviço da base de dados.

        :param instance: Uma instância de um serviço.
        :type instance: Service
        :return: Um booleano que representa se o serviço foi apagado ou não.
        :rtype: bool
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            DELETE FROM Service
            WHERE id=:id
        """, {
            "id": instance.id
        })

        return cursor.rowcount > 0
