import bcrypt

def hash_password(password: str) -> bytes:
    # Convert password to bytes
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password
    )
