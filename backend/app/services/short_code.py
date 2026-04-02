import hashlib
import random
import string
from sqlalchemy.orm import Session
from app.models.link import Link
from app.core.config import settings


def generate_short_code(original_url: str) -> str:
    """Generate short code using SHA1 hash + collision detection."""
    hash_obj = hashlib.sha1(original_url.encode())
    hash_hex = hash_obj.hexdigest()[:settings.SHORT_CODE_LENGTH]

    return hash_hex


def get_unique_short_code(db: Session, original_url: str, preferred_code: str = None) -> str:
    """Get a unique short code, handling collisions."""
    if preferred_code:
        existing = db.query(Link).filter(Link.short_code == preferred_code).first()
        if not existing:
            return preferred_code

    base_code = generate_short_code(original_url)
    code = base_code

    for attempt in range(3):
        existing = db.query(Link).filter(Link.short_code == code).first()
        if not existing:
            return code
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        code = f"{base_code}-{suffix}"

    raise ValueError("Unable to generate unique short code after 3 attempts")


def validate_custom_alias(alias: str) -> bool:
    """Validate custom alias format."""
    if not alias:
        return False
    if len(alias) < 3 or len(alias) > 50:
        return False
    if not alias.replace('-', '').replace('_', '').isalnum():
        return False
    return True
