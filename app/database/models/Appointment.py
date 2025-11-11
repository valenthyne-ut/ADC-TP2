from dataclasses import dataclass
from datetime import date, time

from app.database.models.Base import Base

@dataclass
class Appointment(Base["Appointment"]):
    client_id: int
    technician_id: int
    service_id: int
    date: date
    start_time: time
    end_time: time

    def __str__(self) -> str:
        return f"Informação da marcação:\nID do cliente: {self.client_id}\nID do técnico: {self.technician_id}\nID do serviço: {self.service_id}\nData: {self.date}, das {self.start_time} até às {self.end_time}"