from pydantic import BaseModel

# PUBLIC_INTERFACE
class Settings(BaseModel):
    """Settings for JWT authentication using fastapi-jwt-auth."""
    authjwt_secret_key: str = "secret"  # use env variable in production!
    authjwt_access_token_expires: int = 60 * 24  # minutes (24hr)

# Password hashing helpers using passlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Returns the bcrypt hash for a plain text password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Validates a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)
