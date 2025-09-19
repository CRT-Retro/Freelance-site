import sqlite3

# مسیر دیتابیس و فایل‌های SQL
DB_PATH = "database.db"
SCHEMA_FILE = "schema.sql"
SEED_FILE = "seed.sql"

def create_database():
    """Create database, tables from schema.sql, and insert seed data from seed.sql"""
    # باز کردن connection
    connection = sqlite3.connect(DB_PATH)
    try:
        # اجرای schema
        with open(SCHEMA_FILE, "r") as file:
            sql_script = file.read()
        connection.executescript(sql_script)

        # اجرای seed
        with open(SEED_FILE, "r") as file:
            seed_script = file.read()
        connection.executescript(seed_script)

        connection.commit()
    finally:
        connection.close()

    print("✅ Database ready, tables created, and seed data inserted!")

if __name__ == "__main__":
    create_database()
