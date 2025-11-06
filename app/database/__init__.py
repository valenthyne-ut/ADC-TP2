import sqlite3
from app.database.schema.UserSchema import UserSchema

connection = sqlite3.connect("database.sqlite", autocommit=True)
# connection.set_trace_callback(print)

def initialize_database():
    print("A iniciar base de dados..")
    UserSchema(connection)
    print("Base de dados iniciada.")