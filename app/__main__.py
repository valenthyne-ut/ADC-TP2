from app.database import initialize_database
from app.database.schema.ContactInfoSchema import ContactInfoSchema
from app.database.schema.ServiceSchema import ServiceSchema
from app.database.schema.TechnicianSchema import TechnicianSchema
from app.database.schema.UserSchema import UserSchema

def main():
    initialize_database()

    user = UserSchema.instance.create_one(
        alias="valenthyne.ut", 
        full_name="Valentim U.T."
    )
    
    contact_info = ContactInfoSchema.instance.create_one(
        email="valenthyne.ut@gmail.com", 
        phone_num="+351123456789", 
        address="Rua n sei nº123"
    )
    
    service = ServiceSchema.instance.create_one(
        name="Limpeza de piscina", 
        price=200, 
        duration_mins=240
    )
    
    technician = TechnicianSchema.instance.create_one(
        user_id=user.id, 
        contact_id=contact_info.id, 
        specialization_id=service.id
    )

    print(f"{user}\n\n{contact_info}\n\n{service}\n\n{technician}")

if __name__ == "__main__":
    main()