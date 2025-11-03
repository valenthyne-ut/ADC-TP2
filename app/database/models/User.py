from dataclasses import dataclass
from app.database.models.Base import Base

@dataclass
class User(Base):
    name: str

    def __str__(self) -> str:
        return f"Nome do utilizador: {self.name}"