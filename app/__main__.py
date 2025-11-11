from app.database import initialize_database
from app.database.schema.ClientSchema import ClientSchema
from app.database.schema.ContactInfoSchema import ContactInfoSchema
from app.database.schema.ServiceSchema import ServiceSchema
from app.database.schema.UserSchema import UserSchema

def main():
    initialize_database()

    # user = UserSchema.instance.create_one(
    #     alias="_valenthyne", 
    #     full_name="Valentim U.T."
    # )
    
    # contact_info = ContactInfoSchema.instance.create_one(
    #     email="test-email@googmail.pt", 
    #     phone_num="+351123456789", 
    #     address="Rua do Não Sabedor 123 20ºE"
    # )

    # client = ClientSchema.instance.create_one(
    #     user_id=user.id, 
    #     contact_id=contact_info.id
    # )

    # service = ServiceSchema.instance.create_one(
    #     name="Limpeza da piscina",
    #     price=150.25,
    #     duration_mins=240
    # )

    # print(f"{user}\n\n{contact_info}\n\n{client}\n\n{service}")

    services = ServiceSchema.instance.find_many()
    print(services)

if __name__ == "__main__":
    main()