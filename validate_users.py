import re

def validate_email(email: str) -> bool:
    """Check if email is valid."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def validate_user(user: dict) -> bool:
    """Validate user fields before inserting to database."""
    required_fields = ['username', 'email', 'password_hash', 'role']
    for field in required_fields:
        if field not in user or not user[field].strip():
            print(f"❌ Invalid user: missing {field}")
            return False

    if not validate_email(user['email']):
        print(f"❌ Invalid email: {user['email']}")
        return False

    if user['role'] not in ('freelancer', 'employer', 'admin'):
        print(f"❌ Invalid role: {user['role']}")
        return False

    return True
