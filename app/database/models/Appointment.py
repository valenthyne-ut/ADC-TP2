from dataclasses import dataclass
from datetime import date, time

from app.database.models.Base import Base

@dataclass
class Appointment(Base["Appointment"]):
    client_id: int
    """
    O ID do cliente (:class:`app.database.models.Client`) que realizou a marcação.
    """
    technician_id: int
    """
    O ID do técnico (:class:`app.database.models.Technician`) que acompanhará/acompanhou a marcação.
    """
    service_id: int
    """
    O ID do serviço (:class:`app.database.models.Service`) realizado na marcação.
    """
    date: date
    """
    A data da marcação.
    """
    start_time: time
    """
    A hora de início da marcação.
    """
    end_time: time
    """
    A hora de fim da marcação.
    """

    def __str__(self) -> str:
        return f"Informação da marcação:\nID do cliente: {self.client_id}\nID do técnico: {self.technician_id}\nID do serviço: {self.service_id}\nData: {self.date}, das {self.start_time} até às {self.end_time}"