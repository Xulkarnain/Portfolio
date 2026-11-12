from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import jwt
from jwt import InvalidTokenError

from app.core.config import settings

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Convert a plaintext password into a secure password hash."""
    return password_hash.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify a plaintext password against its stored hash."""
    return password_hash.verify(plain_password, hashed_password)




def create_access_token(subject: str) -> str:
    """Create a signed JWT for an authenticated admin."""
    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(
            minutes=settings.access_token_expire_minutes
        ),
        "iss": settings.app_name,
        "aud": "portfolio-admin",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict | None:
    """Validate a JWT and return its payload."""
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.app_name,
            audience="portfolio-admin",
            options={
                "require": ["sub", "iat", "exp", "iss", "aud"]
            },
        )
    except InvalidTokenError:
        return None

def generate_csrf_token(access_token: str) -> str:
    return hmac.new(
        settings.jwt_secret_key.encode("utf-8"),
        access_token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_csrf_token(
    access_token: str,
    csrf_token: str,
) -> bool:
    expected_token = generate_csrf_token(access_token)

    return hmac.compare_digest(
        expected_token,
        csrf_token,
    )