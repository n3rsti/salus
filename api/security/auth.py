from fastapi import Cookie, HTTPException, status
from typing import Dict, Any, Optional
from jose import JWTError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError

from fastapi import Depends
from sqlmodel import Session, select

from api.database import SessionDep
from api.models.enums import Role
from api.models.user_models import Users

from api.security.jwt import decode_access_token


async def verify_jwt_token(
    access_token: Optional[str] = Cookie(None),
) -> Dict[str, Any]:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No access token provided"
        )
    try:
        payload = decode_access_token(access_token)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except JWTClaimsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid claims"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


class JwtPayload:
    def __init__(self, username: str, email: str, role: int, id: int) -> None:
        self.username: str = username
        self.email: str = email
        self.role: int = role
        self.id: int = id
        pass


async def get_current_user(
    payload: Dict[str, Any] = Depends(verify_jwt_token),
) -> JwtPayload:
    username: str = str(payload.get("username"))
    email: str = str(payload.get("email"))

    raw_role: str = str(payload.get("role"))
    role = int(raw_role)

    raw_id: str = str(payload.get("sub"))
    id = int(raw_id)

    return JwtPayload(username, email, role, id)


def is_admin(jwt: JwtPayload) -> bool:
    return jwt.role == Role.ADMIN or jwt.role == Role.SUPER_ADMIN
