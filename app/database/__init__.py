import sqlite3
from app.database.schema.ClientSchema import ClientSchema
from app.database.schema.ContactInfoSchema import ContactInfoSchema
from app.database.schema.UserSchema import UserSchema

connection = sqlite3.connect("database.sqlite", autocommit=True)
# connection.set_trace_callback(print)

def initialize_database():
    print("A iniciar base de dados..")
    UserSchema(connection)
    ContactInfoSchema(connection)
    ClientSchema(connection)
    print("Base de dados iniciada.")