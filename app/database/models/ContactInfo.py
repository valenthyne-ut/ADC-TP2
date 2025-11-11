from dataclasses import dataclass
from app.database.models.Base import Base


@dataclass
class ContactInfo(Base["ContactInfo"]):
    email: str
    phone_num: str
    address: str | None

    def __str__(self) -> str:
        return f"Informação de contacto:\nE-mail:{self.email}\nNº telemóvel: {self.phone_num}\nEndereço: {self.address if self.address is not None else "Não definido"}"