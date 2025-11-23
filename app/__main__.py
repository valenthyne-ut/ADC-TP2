# from datetime import date, time
from app.database import initialize_database
# from app.database.schema.AppointmentSchema import AppointmentSchema
from app.database.schema.ClientSchema import ClientSchema
from app.database.schema.ContactInfoSchema import ContactInfoSchema
# from app.database.schema.ServiceSchema import ServiceSchema
from app.database.schema.TechnicianSchema import TechnicianSchema
from app.database.schema.UserSchema import UserSchema

from app.criacao_perfis import carregar_dados

def main():
    initialize_database()

    dados = carregar_dados()
    for user in dados.get("Utilizadores"):
        if user is not None:
            db_user = UserSchema.instance.create_one(
                alias=user["Email"],
                full_name=user["Nome"]
            )

            db_contact_info = ContactInfoSchema.instance.create_one(
                email=db_user.alias,
                address=user["Morada"],
                phone_num=user["Contacto"]
            )

            ClientSchema.instance.create_one(
                db_user.id,
                db_contact_info.id
            )

    for technician in dados.get("Técnicos"):
        if technician is not None:
            db_user = UserSchema.instance.create_one(
                alias=technician["Email"],
                full_name=technician["Nome"]
            )

            db_contact_info = ContactInfoSchema.instance.create_one(
                email=db_user.alias,
                address=technician["Morada"],
                phone_num=technician["Contacto"]
            )

            TechnicianSchema.instance.create_one(
                db_user.id,
                db_contact_info.id
            )
    

if __name__ == "__main__":
    main()