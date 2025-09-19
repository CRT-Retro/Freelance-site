import sqlite3
import os

DB_PATH = "database.db"
SCHEMA_FILE = "schema.sql"
SEED_FILE = "seed.sql"

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Old database deleted!")

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")  # فعال‌سازی Foreign Key

        # 1️⃣ Create tables
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("Tables created successfully!")

        # 2️⃣ Insert users first
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            lines = f.read().split(";")
            for line in lines:
                line = line.strip()
                if line.startswith("INSERT INTO users"):
                    conn.execute(line)
        conn.commit()  # 🔹 حتما commit کنیم تا id ها موجود باشن
        print("Users inserted successfully!")

        # 3️⃣ Insert skills
        for line in lines:
            line = line.strip()
            if line.startswith("INSERT INTO skills"):
                conn.execute(line)
        conn.commit()
        print("Skills inserted successfully!")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

    print("✅ Database ready with tables, users, and skills!")

if __name__ == "__main__":
    create_database()
