# This file contains functions for hashing and verifying passwords securely.
# It uses bcrypt through passlib.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_BYTES = 72

def hash_password(password: str) -> str:
    # Hash password with safe truncation to 72 bytes for bcrypt
    truncated = password
    while len(truncated.encode("utf-8")) > MAX_BCRYPT_BYTES:
        truncated = truncated[:-1]
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify password with the same truncation logic
    truncated = plain_password
    while len(truncated.encode("utf-8")) > MAX_BCRYPT_BYTES:
        truncated = truncated[:-1]
    return pwd_context.verify(truncated, hashed_password)
