from dataclasses import dataclass
from app.database.models.Base import Base

@dataclass
class User(Base["User"]):
    alias: str
    """
    O "nome de utilizador".
    """
    full_name: str
    """
    O nome completo do utilizador.
    """

    def __str__(self) -> str:
        return f"Nome do utilizador: {self.alias}"