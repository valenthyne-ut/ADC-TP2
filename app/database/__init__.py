import sqlite3
from app.database.schema.AppointmentSchema import AppointmentSchema
from app.database.schema.ClientSchema import ClientSchema
from app.database.schema.ContactInfoSchema import ContactInfoSchema
from app.database.schema.ServiceSchema import ServiceSchema
from app.database.schema.TechnicianSchema import TechnicianSchema
from app.database.schema.UserSchema import UserSchema

connection = sqlite3.connect("database.sqlite", autocommit=True, detect_types=sqlite3.PARSE_DECLTYPES)
# connection.set_trace_callback(print)

def initialize_database():
    print("A iniciar base de dados..")
    UserSchema(connection)
    ContactInfoSchema(connection)
    ClientSchema(connection)
    ServiceSchema(connection)
    TechnicianSchema(connection)
    ServiceSchema(connection)
    AppointmentSchema(connection)
    print("Base de dados iniciada.")