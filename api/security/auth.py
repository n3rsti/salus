from fastapi import Cookie, HTTPException, status
from typing import Dict, Any, Optional
from jose import JWTError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError

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
