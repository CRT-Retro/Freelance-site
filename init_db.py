import sqlite3
import os

DB_PATH = "database.db"
SCHEMA_FILE = "schema.sql"
SEED_FILE = "seed.sql"
VIEWS_INDEXES_FILE = "views_indexes.sql"

# مهارت‌ها برای هر کاربر
USER_SKILLS = {
    'negin': ['Python', 'Flask', 'Django'],
    'sadra': ['Python', 'Database', 'Pandas'],
    'ali': ['Excel', 'SQL', 'Data Visualization'],
    'sajjad': ['Project Management'],
    'majid': ['Leadership'],
    'radman': ['Database Design', 'SQL'],
    'ronika': ['Backend Development', 'Python'],
    'sedigh': ['Frontend Development', 'HTML/CSS/JS']
}

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Old database deleted!")

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")

        # 1️⃣ ایجاد جداول
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("Tables created successfully!")

        # 2️⃣ اضافه کردن کاربران
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("Users inserted successfully!")

        # 3️⃣ اضافه کردن مهارت‌ها
        cursor = conn.cursor()
        for username, skills in USER_SKILLS.items():
            cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            row = cursor.fetchone()
            if row is None:
                print(f"Warning: user {username} not found!")
                continue
            user_id = row[0]
            for skill in skills:
                cursor.execute(
                    "INSERT INTO skills (user_id, skill) VALUES (?, ?)",
                    (user_id, skill)
                )
        conn.commit()
        print("Skills inserted successfully!")

        # 4️⃣ ایجاد View و Index
        with open(VIEWS_INDEXES_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("Views and indexes created successfully!")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

    print("✅ Database ready with users, skills, views, and indexes!")

if __name__ == "__main__":
    create_database()
