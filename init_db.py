import sqlite3
import os

# Database path and SQL files
DB_PATH = "database.db"
SCHEMA_FILE = "schema.sql"
SEED_FILE = "seed.sql"

def create_database():
    """Create database, tables from schema.sql, and insert seed data from seed.sql"""

    # Delete old database if exists to avoid UNIQUE constraint errors
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Old database deleted!")

    connection = sqlite3.connect(DB_PATH)
    try:
        # Execute schema.sql to create tables
        with open(SCHEMA_FILE, "r") as file:
            sql_script = file.read()
        connection.executescript(sql_script)
        print("Tables created successfully!")

        # Execute seed.sql to insert initial data
        with open(SEED_FILE, "r") as file:
            seed_script = file.read()
        connection.executescript(seed_script)
        print("Seed data inserted successfully!")

        connection.commit()
    except sqlite3.IntegrityError as e:
        print("IntegrityError:", e)
    except Exception as e:
        print("Error:", e)
    finally:
        connection.close()

    print("✅ Database ready with tables and seed data!")

if __name__ == "__main__":
    create_database()
