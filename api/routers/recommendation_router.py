from fastapi import APIRouter, Depends, Query
from typing import Literal

from api.database import SessionDep
from api.security.auth import get_current_user
from api.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("/{user_id}")
def get_recommendations(
    session: SessionDep,
    user_id: int,
    type: Literal["program", "activity"] = Query("program"),
    limit: int = Query(10, ge=1, le=100),
    explain: bool = Query(False),
):
    service = RecommendationService(session)

    return service.get(
        user_id=user_id,
        content_type=type,
        limit=limit,
        explain=explain,
    )
