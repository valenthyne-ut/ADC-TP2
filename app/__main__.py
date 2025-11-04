from app.database import initialize_database
# from app.database.schema.UserSchema import UserSchema

def main():
    initialize_database()

if __name__ == "__main__":
    main()

    # UserSchema.instance.create_one("Teste")
    # user = UserSchema.instance.find_one(1)
    # print(user)