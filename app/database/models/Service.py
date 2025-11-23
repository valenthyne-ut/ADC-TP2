from dataclasses import dataclass
from app.database.models.Base import Base


@dataclass
class Service(Base["Service"]):
    name: str
    """
    O nome do serviço.
    """
    price: float
    """
    O preço do serviço, em euros.
    """
    duration_mins: int
    """
    A duração do serviço, em minutos.
    """

    def __str__(self) -> str:
        return f"ID de serviço: {self.id}\nNome: {self.name}\nPreço: {self.price}\nDuração em minutos: {self.duration_mins}"    