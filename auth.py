import json
import os
import hashlib
import secrets

USERS_FILE = "data/users.json"


def _hash_password(password, salt=None):
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    A random salt is generated for new passwords.
    """
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def _verify_password(password, stored_password):
    """
    Verify a password against a stored PBKDF2 password hash.
    """
    try:
        salt, stored_hash = stored_password.split("$", 1)

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        ).hex()

        return secrets.compare_digest(calculated_hash, stored_hash)

    except (ValueError, AttributeError):
        return False


def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            users = json.load(file)

        if isinstance(users, list):
            return users

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_users(users):
    os.makedirs("data", exist_ok=True)

    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def register_user():
    users = load_users()

    print("\n=== STUDENT REGISTRATION ===")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty.")
        return None

    if len(username) < 3:
        print("Username must contain at least 3 characters.")
        return None

    if len(password) < 6:
        print("Password must contain at least 6 characters.")
        return None

    if any(
        user.get("username", "").lower() == username.lower()
        for user in users
    ):
        print("Username already exists.")
        return None

    users.append({
        "username": username,
        "password": _hash_password(password),
        "role": "student"
    })

    save_users(users)

    print("Registration successful.")
    return username


def login_user():
    users = load_users()

    print("\n=== STUDENT LOGIN ===")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    for user in users:

        if user.get("username", "").lower() != username.lower():
            continue

        if user.get("role") != "student":
            continue

        if _verify_password(password, user.get("password", "")):
            print("Login successful.")
            return user

    print("Invalid username or password.")
    return None


def admin_login():
    print("\n=== ADMIN LOGIN ===")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    admin_user = os.getenv(
        "QUIZMASTER_ADMIN_USER",
        "admin"
    )

    admin_password = os.getenv(
        "QUIZMASTER_ADMIN_PASSWORD",
        "admin123"
    )

    if username == admin_user and password == admin_password:

        print("Admin login successful.")

        return {
            "username": username,
            "role": "admin"
        }

    print("Invalid admin credentials.")
    return None


def logout_user(user):
    """
    End the current user's session.
    """
    if user:
        print(f"{user.get('username', 'User')} has been logged out.")

    return None
