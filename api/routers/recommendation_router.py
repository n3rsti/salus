from fastapi import APIRouter, Depends, Query
from typing import Literal

from api.database import SessionDep
from api.security.auth import get_current_user
from api.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

#testy
from sqlmodel import select
from api.models.user_preference_models import UserPreference
from api.models.user_activity_models import UserActivity
from api.models.tag_models import Tag
from api.models.programs_tags_link import ProgramTagLink
#testy

#vvvvvv default i think?? vvvv
# @router.get("")
# def get_recommendations(
#     session: SessionDep,
#     type: Literal["program", "activity"] = Query("program"),
#     limit: int = Query(10, ge=1, le=20),
#     explain: bool = Query(False),
#     user=Depends(get_current_user),
# ):
#     service = RecommendationService(session)

#     return service.get(
#         user_id=user.id,
#         content_type=type,
#         limit=limit,
#         explain=explain,
#     )

@router.get("/{user_id}")
def get_recommendations(
    session: SessionDep,
    user_id: int,
    type: Literal["program", "activity"] = Query("program"),
    limit: int = Query(10, ge=1, le=20),
    explain: bool = Query(False),
):
    service = RecommendationService(session)

    return service.get(
        user_id=user_id,
        content_type=type,
        limit=limit,
        explain=explain,
    )


# @router.get("/{program_id}")
# def test(session: SessionDep, program_id: int):
#     rows = session.exec(
#         select(Tag.name)
#         .join(ProgramTagLink, ProgramTagLink.tag_id == Tag.id)
#         .where(ProgramTagLink.program_id == program_id)
#     ).all()

#     return rows