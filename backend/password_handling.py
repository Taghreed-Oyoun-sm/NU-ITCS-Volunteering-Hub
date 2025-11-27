from passlib.context import CryptContext

# Constants & CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_BYTES = 72

# Hash a password safely

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt, safely truncated to 72 bytes.
    """
    # Truncate password so that its UTF-8 encoded length <= MAX_BCRYPT_BYTES
    truncated = password
    while len(truncated.encode("utf-8")) > MAX_BCRYPT_BYTES:
        truncated = truncated[:-1]
    return pwd_context.hash(truncated)

# Verify a password safely

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password using bcrypt, truncating safely to 72 bytes.
    """
    truncated = plain_password
    while len(truncated.encode("utf-8")) > MAX_BCRYPT_BYTES:
        truncated = truncated[:-1]
    return pwd_context.verify(truncated, hashed_password)
