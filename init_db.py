import sqlite3

DB_PATH = "database.db"
SCHEMA_FILE = "schema.sql"

def create_database():
    """Create database and tables from schema.sql"""
    with open(SCHEMA_FILE, "r") as file:
        sql_script = file.read()

    connection = sqlite3.connect(DB_PATH)
    try:
        connection.executescript(sql_script)
        connection.commit()
    finally:
        connection.close()

    print("Database ready and tables created!")

if __name__ == "__main__":
    create_database()
