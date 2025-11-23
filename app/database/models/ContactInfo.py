from dataclasses import dataclass
from app.database.models.Base import Base


@dataclass
class ContactInfo(Base["ContactInfo"]):
    email: str
    """
    O e-mail contido na informação de contactos.
    """
    phone_num: str
    """
    O número de telefone/telemóvel contido na informação de contactos.
    """
    address: str | None
    """
    O endereço contido an informação de contactos.
    """

    def __str__(self) -> str:
        return f"Informação de contacto:\nE-mail:{self.email}\nNº telemóvel: {self.phone_num}\nEndereço: {self.address if self.address is not None else "Não definido"}"