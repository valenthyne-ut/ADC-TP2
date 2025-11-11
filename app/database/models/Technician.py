from dataclasses import dataclass
from app.database.models.Base import Base

@dataclass
class Technician(Base["Technician"]):
    contact_id: int
    specialization_id: int

    def __str__(self) -> str:
        return f"ID de utilizador: {self.id}\nID de informação de contacto: {self.contact_id}\nID de especialização: {self.specialization_id}"