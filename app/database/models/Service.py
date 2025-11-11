from dataclasses import dataclass
from app.database.models.Base import Base


@dataclass
class Service(Base["Service"]):
    name: str
    price: float
    duration_mins: int

    def __str__(self) -> str:
        return f"ID de serviço: {self.id}\nNome: {self.name}\nPreço: {self.price}\nDuração em minutos: {self.duration_mins}"    