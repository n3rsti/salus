import pytest
from datetime import timedelta
from api.security.jwt import create_access_token, decode_access_token

# Dummy test data
TEST_SUBJECT = "12345"
TEST_CLAIMS = {"email": "test@example.com", "role": "user"}


def test_jwt_creation_and_decoding():
    # Create token
    token = create_access_token(
        subject=TEST_SUBJECT,
        expires_delta=timedelta(minutes=10),
        extra_claims=TEST_CLAIMS,
    )

    assert isinstance(token, str)
    assert token.count(".") == 2  # Basic JWT format check

    # Decode token
    payload = decode_access_token(token)

    # Verify claims
    assert payload["sub"] == TEST_SUBJECT
    assert payload["email"] == "test@example.com"
    assert payload["role"] == "user"
    assert "exp" in payload  # expiration must exist


def test_jwt_expiration(monkeypatch):
    """Test that expired tokens raise an exception."""
    from datetime import datetime, timezone
    from jose import ExpiredSignatureError

    # Monkeypatch datetime to simulate old token
    class FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2020, 1, 1, tzinfo=timezone.utc)

    monkeypatch.setattr("api.security.jwt.datetime", FixedDatetime)

    # Create token that expired long ago
    token = create_access_token(TEST_SUBJECT, expires_delta=timedelta(seconds=1))

    # Reset datetime to real now
    from api.security import jwt as jwt_module

    monkeypatch.setattr(jwt_module, "datetime", datetime)

    # Try decoding, expect ExpiredSignatureError
    with pytest.raises(ExpiredSignatureError):
        decode_access_token(token)
