from datetime import date, time
from app.database import initialize_database
from app.database.schema.AppointmentSchema import AppointmentSchema
from app.database.schema.ClientSchema import ClientSchema
from app.database.schema.ContactInfoSchema import ContactInfoSchema
from app.database.schema.ServiceSchema import ServiceSchema
from app.database.schema.TechnicianSchema import TechnicianSchema
from app.database.schema.UserSchema import UserSchema

def main():
    initialize_database()

    user1 = UserSchema.instance.create_one(
        alias="valenthyne.ut", 
        full_name="Valentim U.T."
    )

    user2 = UserSchema.instance.create_one(
        alias="marino.nc", 
        full_name="Marino N.C."
    )

    contact_info1 = ContactInfoSchema.instance.create_one(
        email="valenthyne.ut@gmail.com", 
        phone_num="+351123456789", 
        address="Rua n sei nº123"
    )

    contact_info2 = ContactInfoSchema.instance.create_one(
        email="marinonechifor@googmail.pt", 
        phone_num="+351987654321", 
        address="Rua acolá nº123"
    )
    
    service = ServiceSchema.instance.create_one(
        name="Limpeza de piscina", 
        price=200, 
        duration_mins=240
    )
    
    technician = TechnicianSchema.instance.create_one(
        user_id=user1.id, 
        contact_id=contact_info1.id, 
        specialization_id=service.id
    )

    client = ClientSchema.instance.create_one(
        user_id=user2.id,
        contact_id=contact_info2.id
    )

    AppointmentSchema.instance.create_one(
        client_id=client.id,
        technician_id=technician.id,
        service_id=service.id,
        date=date.fromisoformat("2025-11-20"),
        start_time=time.fromisoformat("12:00:00"),
        end_time=time.fromisoformat("16:00:00")
    )

if __name__ == "__main__":
    main()