from app.database import initialize_database

from app.database.schema.UserSchema import UserSchema

def main():
    initialize_database()

if __name__ == "__main__":
    main()
    
    #UserSchema.instance.create_one("alias de teste", "nome de teste")
    print(UserSchema.instance.find_one(alias="teste"))
    print(UserSchema.instance.find_many())