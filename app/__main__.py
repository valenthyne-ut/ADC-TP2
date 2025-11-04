from app.database import initialize_database
from app.database.schema.UserSchema import UserSchema

def main():
    initialize_database()

if __name__ == "__main__":
    main()

    user = UserSchema.instance.create_one("Teste")
    UserSchema.instance.find_one(user.id)