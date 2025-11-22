from abc import ABC, abstractmethod
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Any, Generic, Literal

from app.database.models.Base import T

@dataclass
class Filter:
    """
    Uma classe que representa um filtro de pesquisa, para auxiliar com a 
    criação de queries.
    """
    name: str
    """
    O nome da coluna a filtrar.
    """
    value: Any
    """
    O valor da coluna a filtrar.
    """
    comparison_operator: Literal["=", "<>", "!=", "<", "<=", ">=", ">", "LIKE"] = "="
    """
    O operador de comparação a ser utilizado no filtro. São utilizáveis 
    alguns dos operadoes presentes no motor de bases de dados SQLite.
    """
    logical_operator: Literal["AND", "OR", "NOT"] = "AND"
    """
    O operador lógico a utilizar após ser criada a cláusula de filtro.
    Se for o primeiro filtro na sequência, este parâmetro é ignorado.
    """

class BaseSchema(ABC, Generic[T]):
    def __init__(self, connection: Connection):
        self._connection = connection

    def _table_exists(self, table_name: str) -> bool:
        """
        Verifica se uma tabela existe na base de dados.

        :param table_name: O nome da tabela a verificar.
        :type table_name: str
        :return: Um booleano que representa se existe ou não a tabela.
        :rtype: bool
        """
        cursor = self._connection.cursor()
        result = cursor.execute("""
            SELECT name 
            FROM sqlite_master
            WHERE type='table' AND name=:name
        """, {
            "name": table_name
        }).fetchall()

        return len(result) > 0

    @staticmethod
    def _construct_basic_filter_clause(filters: list[Filter]) -> tuple[str, dict[str, Any]]:
        """
        Constroi um conjunto de filtros para utilização numa cláusula WHERE.

        :param filters: O conjunto de filtros.
        :type filters: list[Filter]
        :return: 
            Uma ``tuple`` que contém a query preparada e um dicionário que 
            contém os nomes das colunas e os valores correspondentes a pesquisar,
            a serem utilizados num método ``cursor.execute(sql, parameters)``.
        :rtype: tuple[str, dict[str, Any]]
        :raises ValueError: Se o parâmetro filters estiver vazio.
        """
        if len(filters) <= 0:
            raise ValueError("O argumento 'filters' tem de ter pelo menos um valor!")
        
        clause = ""
        params: dict[str, Any] = {}

        for index, filter in enumerate(filters):
            if filter.value is not None:
                lop = filter.logical_operator if index > 0 else ""
                name = filter.name
                value = filter.value
                cop = filter.comparison_operator

                clause = f"{clause} {lop} {name} {cop} :{name}"
                if cop == "LIKE" and isinstance(value, str):
                    value = f"%{value}%"

                params[name] = value

        return clause, params

    @abstractmethod
    def find_one(self) -> T | None:
        """
        Um método abstrato a ser implementado pelo utilizador.
        Pesquisa por um resultado de uma tabela na base de dados.

        :return: O resultado correspondende à tabela, se for encontrado.
        :rtype: T | None
        """
        ...

    @abstractmethod
    def find_many(self, limit: int = 2000) -> list[T]:
        """
        Um método abstrato a ser implementado pelo utilizador.
        Pesquisa por vários resultados de uma tabela na base de dados.

        :param limit: O número máximo de resultados a devolver. 
        :type limit: int = 2000
        :return: Uma lista de resultados correspondende à tabela, se algum for encontrado.
        :rtype: list[T]
        """
        ...

    @abstractmethod
    def create_one(self) -> T:
        """
        Um método abstrato a ser implementado pelo utilizador.
        Insere um valor numa tabela na base de dados e devolve esse mesmo.

        :return: O valor correspondende à tabela.
        :rtype: T
        """
        ...

    @abstractmethod
    def delete(self, instance: T) -> bool:
        """
        Um método abstrato a ser implementado pelo utilizador.
        Apaga um valor de uma tabela na base de dados.

        :param instance: Uma instância de uma tabela.
        :type instance: T
        :return: Um booleano que representa se esse valor foi apagado ou não.
        :rtype: bool
        """
        ...