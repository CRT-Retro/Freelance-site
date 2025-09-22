import re
import sqlite3

DB_PATH = "database.db"

# Regex برای ایمیل معتبر
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def is_valid_email(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None

def is_valid_password(password: str) -> bool:
    return len(password) >= 6

def register_user(username: str, email: str, password: str, role="freelancer", job_title=None, location=None):
    """ثبت‌نام کاربر با اعتبارسنجی ایمیل و پسورد"""
    if not is_valid_email(email):
        print("❌ ایمیل معتبر نیست")
        return

    if not is_valid_password(password):
        print("❌ پسورد باید حداقل 6 کاراکتر باشد")
        return

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role, job_title, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, email, password, role, job_title, location))
        connection.commit()
        print("✅ کاربر با موفقیت ثبت شد")
    except sqlite3.IntegrityError as e:
        print("❌ خطا: ", e)
    finally:
        connection.close()

if __name__ == "__main__":
    # تست نمونه
    register_user("new_user", "new_user@example.com", "mypassword", "freelancer", "Tester", "Tehran")
