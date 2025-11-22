from datetime import date, time

from sqlite3 import Connection

from app.database.models.Appointment import Appointment
from app.database.schema.BaseSchema import BaseSchema, Filter

class AppointmentSchema(BaseSchema["Appointment"]):
    instance: "AppointmentSchema"

    def __init__(self, connection: Connection):
        super().__init__(connection)
        if not self._table_exists("Appointment"):
            if not self._table_exists("Client"):
                raise LookupError("Tabela de Client não existe, sendo a Appointment dependente dela. Tente reiniciar a base de dados.")
            
            if not self._table_exists("Technician"):
                raise LookupError("Tabela de Technician não existe, sendo a Appointment dependente dela. Tente reiniciar a base de dados.")

            if not self._table_exists("Service"):
                raise LookupError("Tabela de Service não existe, sendo a Appointment dependente dela. Tente reiniciar a base de dados.")

            cursor = self._connection.cursor()
            cursor.execute("""
                CREATE TABLE Appointment(
                    id INTEGER NOT NULL PRIMARY KEY,
                    client_id INTEGER NOT NULL,
                    technician_id INTEGER NOT NULL,
                    service_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    start_time TIME NOT NULL,
                    end_time TIME NOT NULL
                )
            """)
        AppointmentSchema.instance = self

    def find_one(self, id: int | None = None, date: date | None = None, client_id: int | None = None, 
                technician_id: int | None = None, service_id: int | None = None) -> Appointment | None:
        """
        Pesquisa por uma marcação na base de dados utilizando os filtros fornecidos.
        Pelo menos um dos filtros tem de ser fornecido.

        :param id: O ID único da marcação. **Este filtro invalida todos os outros.** 
        :param date: A data da marcação.
        :param client_id: O ID único do cliente que realizou a marcação.
        :param technician_id: O ID único do técnico que participará na marcação.
        :param service_id: O ID único do serviço que irá ser realizado na marcação.
        :type id: int
        :type date: int
        :type client_id: int
        :type technician_id: int
        :type service_id: int
        :return: A marcação, se for encontrada.
        :rtype: Appointment | None
        :raises ValueError: Se nenhum filtro for fornecido.
        """
        if id is None and date is None and client_id is None and technician_id is None and service_id is None:
            raise ValueError("Um parâmetro dos 'id', 'date', 'client_id', 'technician_id' ou 'service_id' tem de ser especificado!")

        base_query = """
            SELECT id, client_id, technician_id, service_id, date, start_time, end_time
            FROM Appointment
        """

        query = base_query

        clause, params = BaseSchema._construct_basic_filter_clause([
            Filter("date", date, "="),
            Filter("client_id", client_id, "="),
            Filter("technician_id", technician_id, "="),
            Filter("service_id", service_id, "=")
        ])

        if len(clause) > 0:
            query = f"{query} WHERE {clause} LIMIT 1"

        if id is not None:
            query = f"{base_query} WHERE id=:id"
            params.clear()
            params["id"] = id

        cursor = self._connection.cursor()
        result = cursor.execute(query, params).fetchone()

        return Appointment(result[0], result[1], result[2], result[3], result[4], result[5], result[6])

    def find_many(self, limit: int = 2000, date: date | None = None, client_id: int | None = None, 
                technician_id: int | None = None, service_id: int | None = None) -> list[Appointment]:
        """
        Pesquisa por várias marcações na base de dados utilizando os filtros fornecidos.

        :param limit: O número máximo de marcações a devolver. 
        :param date: A data da(s) marcação(ões).
        :param client_id: O ID único do cliente que realizou a(s) marcação(ões).
        :param technician_id: O ID único do técnico que participará na(s) marcação(ões).
        :param service_id: O ID único do serviço que irá ser realizado na(s) marcação(ões).
        :type limit: int = 2000
        :type date: int
        :type client_id: int
        :type technician_id: int
        :type service_id: int
        :return: Uma lista de marcações, se alguma for encontrada.
        :rtype: list[Appointment]
        """
        cursor = self._connection.cursor()

        base_query = """
            SELECT id, client_id, technician_id, service_id, date, start_time, end_time
            FROM Appointment
        """

        query = base_query

        clause, params = BaseSchema._construct_basic_filter_clause([
            Filter("date", date, "="),
            Filter("client_id", client_id, "="),
            Filter("technician_id", technician_id, "="),
            Filter("service_id", service_id, "=")
        ])

        if len(clause) > 0:
            query = f"{query} WHERE {clause}"

        query = f"{query} LIMIT :limit"
        params["limit"] = limit

        result = cursor.execute(query, params).fetchall()

        appointment_list: list[Appointment] = []

        for item in result:
            appointment_list.append(Appointment(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))

        return appointment_list

    def create_one(self, client_id: int | None = None, technician_id: int | None = None, service_id: int | None = None, 
                    date: date | None = None, start_time: time | None = None, end_time: time | None = None) -> Appointment:
        """
        Insere uma nova marcação na base de dados e devolve a mesma.

        :param client_id: O ID único do cliente que realizou a marcação.
        :param technician_id: O ID único do técnico que participará na marcação.
        :param service_id: O ID único do serviço que irá ser realizado na marcação.
        :param date: A data da marcação.
        :param start_time: A hora de início da marcação.
        :param end_time: A hora de fim da marcação.
        :type client_id: int
        :type technician_id: int
        :type service_id: int
        :type date: int
        :type start_time: time
        :type end_time: time
        :return: A marcação criada.
        :rtype: Appointment
        :raises ValueError: Se faltar qualquer informação necessária à criação de uma marcação.
        :raises ValueError: Se correr mal a inserção da marcação na base de dados.
        """
        if client_id is None or technician_id is None or service_id is None or date is None or start_time is None or end_time is None:
            raise ValueError("Todos os parâmetros 'client_id', 'technician_id', 'service_id', 'date', 'start_time' e 'end_time' têm de ser especificados!")

        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO Appointment(client_id, technician_id, service_id, date, start_time, end_time)
            VALUES(:client_id, :technician_id, :service_id, :date, :start_time, :end_time)
        """, {
            "client_id": client_id,
            "technician_id": technician_id,
            "service_id": service_id,
            "date": date,
            "start_time": str(start_time),
            "end_time": str(end_time)
        })

        if cursor.lastrowid is None:
            raise ValueError("Algo correu mal ao inserir os dados!")

        return Appointment(cursor.lastrowid, client_id, technician_id, service_id, date, start_time, end_time)

    def delete(self, instance: Appointment) -> bool:
        """
        Apaga uma marcação da base de dados.

        :param instance: A instância da marcação.
        :type instance: Appointment
        :return: Um booleano que indica se foi ou não removida a marcação.
        :rtype: bool
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            DELETE FROM Appointment
            WHERE id=:id
        """, {
            "id": instance.id
        })

        return cursor.rowcount > 0