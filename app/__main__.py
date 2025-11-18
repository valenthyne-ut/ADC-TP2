from datetime import date, time
from app.database import initialize_database
from app.database.schema.AppointmentSchema import AppointmentSchema
from app.database.schema.ClientSchema import ClientSchema
from app.database.schema.ContactInfoSchema import ContactInfoSchema
from app.database.schema.ServiceSchema import ServiceSchema
from app.database.schema.TechnicianSchema import TechnicianSchema
from app.database.schema.UserSchema import UserSchema

from app.criacao_perfis import carregar_dados

def main():
    initialize_database()

    dados = carregar_dados()
    for user in dados.get("Utilizadores"):
        UserSchema.instance.create_one(
            alias=user["Email"],
            full_name=user["Nome"]
        )
        
    for user in dados.get("Técnicos"):
        UserSchema.instance.create_one(
            alias=user["Email"],
            full_name=user["Nome"]
        )
    

if __name__ == "__main__":
    main()