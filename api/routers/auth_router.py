import re
import urllib.parse
from typing import Any
import httpx
from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select, or_
from api.database import SessionDep
from dotenv import dotenv_values
from api.models.enums import Role
from api.models.user_models import Users
from api.security.jwt import create_access_token
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


# This file contains API endpoints related to authentication via Google OAuth2.0

router = APIRouter(prefix="/api/auth", tags=["Auth"])
ph = PasswordHasher()

_env = dotenv_values(".env")
GOOGLE_CLIENT_ID = _env.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = _env.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = _env.get("GOOGLE_REDIRECT_URI")

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_SCOPES = "openid email profile"
DEFAULT_ROLE_NAME = "user"


def _generate_unique_username(session: SessionDep, seed: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", seed.lower()).strip("_") or "user"
    candidate = base
    counter = 1

    while session.exec(select(Users).where(Users.username == candidate)).first():
        candidate = f"{base}_{counter}"
        counter += 1

    return candidate


def _ensure_oauth_configured() -> None:
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET or not GOOGLE_REDIRECT_URI:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth credentials are not configured",
        )


@router.get("/google/login")
def google_login() -> dict[str, str]:
    _ensure_oauth_configured()

    query = urllib.parse.urlencode(
        {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": GOOGLE_SCOPES,
            "access_type": "offline",
            "prompt": "consent",
        }
    )
    authorization_url = f"{GOOGLE_AUTH_ENDPOINT}?{query}"
    return {"authorization_url": authorization_url}


async def _exchange_code_for_tokens(code: str) -> dict[str, Any]:
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GOOGLE_TOKEN_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to exchange authorization code",
        )

    return response.json()


async def _fetch_userinfo(access_token: str) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GOOGLE_USERINFO_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=15,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch Google user info",
        )

    return response.json()


def _upsert_user_from_google(session: SessionDep, userinfo: dict[str, Any]) -> Users:
    google_sub = userinfo.get("sub")
    email = userinfo.get("email")
    name = userinfo.get("name") or email or f"google-{google_sub}"

    user = None
    if google_sub:
        user = session.exec(
            select(Users).where(
                Users.oauth_provider == "google", Users.oauth_sub == google_sub
            )
        ).first()

    if not user and email:
        user = session.exec(select(Users).where(Users.email == email)).first()

    if user:
        user.oauth_provider = "google"
        user.oauth_sub = google_sub
        if email and not user.email:
            user.email = email
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    role_id = Role.USER

    username = _generate_unique_username(session, name)

    user = Users(
        username=username,
        email=email,
        role_id=role_id,
        password=None,
        oauth_provider="google",
        oauth_sub=google_sub,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/google/callback")
async def google_callback(code: str, session: SessionDep):
    _ensure_oauth_configured()

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing code"
        )

    tokens = await _exchange_code_for_tokens(code)
    access_token = tokens.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google token response missing access_token",
        )

    userinfo = await _fetch_userinfo(access_token)
    user = _upsert_user_from_google(session, userinfo)

    jwt_token = create_access_token(
        subject=str(user.id),
        extra_claims={
            "username": user.username,
            "email": user.email or "",
            "provider": "google",
        },
    )

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }


@router.post("/login", status_code=status.HTTP_200_OK)
def classic_login(
    payload: LoginRequest,
    response: Response,
    session: SessionDep,
):
    user = session.exec(
        select(Users).where(
            or_(
                Users.username == payload.username_or_email,
                Users.email == payload.username_or_email,
            )
        )
    ).first()

    if not user or not user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    try:
        ph.verify(user.password, payload.password)
    except VerifyMismatchError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token(
        subject=str(user.id),
        extra_claims={
            "username": user.username,
            "email": user.email or "",
            "role": user.role_id,
        },
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # set True in prod
        samesite="lax",
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role_id,
            "email": user.email,
        },
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}
