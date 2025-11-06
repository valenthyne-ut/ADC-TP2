from dataclasses import dataclass
from app.database.models.Base import Base

@dataclass
class User(Base["User"]):
    alias: str
    full_name: str

    def __str__(self) -> str:
        return f"Nome do utilizador: {self.alias}"