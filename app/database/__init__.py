import sqlite3

connection = sqlite3.connect("database.sqlite")

def initialize_database():
    cursor = connection.cursor()
    result = cursor.execute("SELECT 1=1;")
    print(result.fetchone())