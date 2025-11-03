import sqlite3
from app.database.schema.UserSchema import UserSchema

connection = sqlite3.connect("database.sqlite")

def initialize_database():
    print("A iniciar base de dados..")
    UserSchema(connection)
    print("Base de dados iniciada.")