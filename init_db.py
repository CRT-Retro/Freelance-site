import sqlite3
import os
from validate_users import validate_user

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

def load_seed_users(file_path):
    """Load users from seed.sql and return as list of dicts."""
    users = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # جدا کردن هر خط INSERT
    insert_statements = [stmt.strip() for stmt in content.split('VALUES') if stmt.strip()]
    if len(insert_statements) > 1:
        values_part = insert_statements[1]
        # حذف پرانتزهای اضافی و ; آخر
        values_part = values_part.strip().rstrip(';')
        entries = values_part.split('),')
        for entry in entries:
            entry = entry.replace('(', '').replace(')', '').replace("'", "")
            parts = [p.strip() for p in entry.split(',')]
            user = {
                'username': parts[0],
                'email': parts[1],
                'password_hash': parts[2],
                'role': parts[3],
                'job_title': parts[4],
                'location': parts[5]
            }
            users.append(user)
    return users

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

        # 2️⃣ درج کاربران از seed.sql با اعتبارسنجی
        users = load_seed_users(SEED_FILE)
        cursor = conn.cursor()
        for user in users:
            if validate_user(user):
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, role, job_title, location) VALUES (?, ?, ?, ?, ?, ?)",
                    (user['username'], user['email'], user['password_hash'], user['role'], user['job_title'], user['location'])
                )
        conn.commit()
        print("Users inserted successfully!")

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
