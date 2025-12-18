from fastapi import Cookie, HTTPException, status
from typing import Dict, Any, Optional
from jose import JWTError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError

from fastapi import Depends
from sqlmodel import Session, select

from api.database import SessionDep
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

async def get_current_user(
    session: SessionDep,
    payload: Dict[str, Any] = Depends(verify_jwt_token),
) -> Users:
    user_id = payload.get("sub")

    user = session.exec(
        select(Users).where(Users.id == int(user_id))
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user