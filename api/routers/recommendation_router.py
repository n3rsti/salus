from fastapi import APIRouter, Depends, Query
from typing import Literal

from api.database import SessionDep
from api.security.auth import get_current_user
from api.services.recommendation_service import RecommendationService
from api.security.auth import JwtPayload, get_current_user

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("/{type}/{limit}")
def get_recommendations(
    session: SessionDep,
    type: Literal["program", "activity"],
    limit: int,
    explain: bool = Query(True),
    current_user: JwtPayload = Depends(get_current_user),
):

    service = RecommendationService(session)

    return service.get(
        user_id=current_user.id,
        content_type=type,
        limit=limit,
        explain=explain,
    )
