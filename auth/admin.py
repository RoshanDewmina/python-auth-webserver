from passlib.context import CryptContext

hash_helper = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Admin DB
admin_db = {"admin@example.com": hash_helper.hash("password123")}

def validate_admin(email: str, password: str) -> bool:
    if email in admin_db and hash_helper.verify(password, admin_db[email]):
        return True
    return False

