from dataclasses import dataclass
from app.database.models.Base import Base

@dataclass
class Technician(Base["Technician"]):
    contact_id: int
    """
    O ID da informação de contacto (:class:`app.database.models.ContactInfo`) do técnico.
    """
    specialization_id: int
    """
    O ID da especialização (:class:`app.database.models.Service`) do técnico.
    """

    def __str__(self) -> str:
        return f"ID de utilizador: {self.id}\nID de informação de contacto: {self.contact_id}\nID de especialização: {self.specialization_id}"