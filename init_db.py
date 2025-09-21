import sqlite3
import os
import re

# مسیر دیتابیس و فایل‌ها
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

# ------------------ Validation Helpers ------------------
def validate_email(email: str) -> bool:
    """Check if email format is valid using regex"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_username(username: str) -> bool:
    """Username must be at least 3 chars and no spaces"""
    return len(username) >= 3 and " " not in username

def validate_password(password: str) -> bool:
    """Password must be at least 6 characters"""
    return len(password) >= 6
# --------------------------------------------------------

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

        # 2️⃣ درج کاربران
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("Users inserted successfully!")

        # 🔍 اعتبارسنجی داده‌های درج‌شده
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, password_hash FROM users")
        for user_id, username, email, password in cursor.fetchall():
            if not validate_username(username):
                raise ValueError(f"❌ Invalid username: {username}")
            if not validate_email(email):
                raise ValueError(f"❌ Invalid email: {email}")
            if not validate_password(password):
                raise ValueError(f"❌ Invalid password for user {username}")
        print("✅ All users validated successfully!")

        # 3️⃣ درج مهارت‌ها
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

        # 4️⃣ ایجاد View و Indexes
        if os.path.exists(VIEWS_INDEXES_FILE):
            with open(VIEWS_INDEXES_FILE, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            print("Views and indexes created successfully!")
        else:
            print("⚠️ No views_indexes.sql file found, skipped.")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

    print("✅ Database ready with users, skills, views, and indexes!")

if __name__ == "__main__":
    create_database()
