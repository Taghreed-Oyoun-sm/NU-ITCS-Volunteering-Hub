from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_BYTES = 150

def hash_password(password: str) -> str:
    truncated = password
    while len(truncated.encode("utf-8")) > MAX_BCRYPT_BYTES:
        truncated = truncated[:-1]
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = plain_password
    while len(truncated.encode("utf-8")) > MAX_BCRYPT_BYTES:
        truncated = truncated[:-1]
    return pwd_context.verify(truncated, hashed_password)
