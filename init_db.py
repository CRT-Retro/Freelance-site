import sqlite3
import os
import re

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
    'sedigh': ['Frontend Development', 'HTML/CSS/JS'],
    'mohammad': ['Python', 'SQL']  # مثال مهارت برای کاربر جدید
}

# الگوی ساده برای اعتبارسنجی ایمیل
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

def create_database():
    # حذف دیتابیس قدیمی
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Old database deleted!")
    else:
        print("No old database found, creating a new one...")

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")

        # 1️⃣ ایجاد جداول
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("Tables created successfully!")

        cursor = conn.cursor()

        # 2️⃣ درج کاربران از seed.sql با اعتبارسنجی ایمیل
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith("INSERT INTO users"):
                values_str = line[line.find("VALUES")+6:].strip().rstrip(';')
                users_list = values_str.split("),")
                for user_str in users_list:
                    user_str = user_str.strip().lstrip('(').rstrip(')')
                    fields = [f.strip().strip("'") for f in user_str.split(",")]
                    if len(fields) < 6:
                        print(f"❌ Skipping invalid user entry: {user_str}")
                        continue
                    username, email, password_hash, role, job_title, location = fields
                    # اعتبارسنجی ایمیل
                    if not re.match(EMAIL_REGEX, email):
                        print(f"❌ Invalid email: {email}")
                        continue
                    cursor.execute(
                        "INSERT INTO users (username, email, password_hash, role, job_title, location) VALUES (?, ?, ?, ?, ?, ?)",
                        (username, email, password_hash, role, job_title, location)
                    )
        conn.commit()
        print("✅ Users inserted successfully!")

        # 3️⃣ درج مهارت‌ها با Python
        for username, skills in USER_SKILLS.items():
            cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            if result:
                user_id = result[0]
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
