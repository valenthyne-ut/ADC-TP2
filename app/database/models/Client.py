from dataclasses import dataclass
from app.database.models.Base import Base

@dataclass
class Client(Base["Client"]):
    contact_id: int
    """
    O ID da informação de contactos (:class:`app.database.models.ContactInfo`) do cliente.
    """

    def __str__(self) -> str:
        return f"ID de utilizador: {self.id}\nID de informação de contacto: {self.contact_id}"