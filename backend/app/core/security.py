from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from app.core.config import settings

# Token type constants
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def _truncate_password(password: str) -> bytes:
    # bcrypt max input is 72 bytes
    encoded = password.encode('utf-8')
    if len(encoded) <= 72:
        return encoded
    return encoded[:72]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = _truncate_password(plain_password)
    return bcrypt.checkpw(truncated, hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    truncated = _truncate_password(password)
    return bcrypt.hashpw(truncated, bcrypt.gensalt()).decode('utf-8')


def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    delta = expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(data, delta, ACCESS_TOKEN_TYPE)


def create_refresh_token(data: dict) -> str:
    return create_token(data, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), REFRESH_TOKEN_TYPE)


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
