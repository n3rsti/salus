from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from dotenv import dotenv_values
from jose import JWTError, jwt

# This file handles JWT token generation used for user authentication.
# It loads configuration from .env and provides a helper to create signed access tokens with custom claims.
# When running in Docker, the environment variables, should be injected through the container, not directly by the .env file.

_env = dotenv_values(".env")

SECRET_KEY: str = _env.get("JWT_SECRET_KEY", "change-me")
ALGORITHM: str = _env.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    _env.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[Dict[str, Any]] = None,
) -> str:
    # Create a signed JWT access token.
    to_encode: Dict[str, Any] = {"sub": subject}
    if extra_claims:
        to_encode.update(extra_claims)

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    # Decode and validate a JWT access token.
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
