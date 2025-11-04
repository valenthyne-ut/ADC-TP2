from app.database import initialize_database

from app.database.schema.UserSchema import UserSchema

def main():
    initialize_database()

if __name__ == "__main__":
    main()

    # for i in range(1, 10):
    #    UserSchema.instance.create_one(f"Teste {i}")
    
    print(UserSchema.instance.find_many())
    # print(user)