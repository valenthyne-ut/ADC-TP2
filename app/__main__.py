from app.database import initialize_database

from app.database.schema.UserSchema import UserSchema

def main():
    initialize_database()

if __name__ == "__main__":
    main()
    
    print("Antes de apagar:\n", UserSchema.instance.find_many())

    user_to_delete = UserSchema.instance.find_one(id=2)
    if user_to_delete is not None:
        print(UserSchema.instance.delete(user_to_delete))

    print("Depois de apagar:\n", UserSchema.instance.find_many())