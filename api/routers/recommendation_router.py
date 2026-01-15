from fastapi import APIRouter, Depends, Query
from typing import Literal

from api.database import SessionDep
from api.security.auth import get_current_user
from api.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

#testy
from sqlmodel import select
from sqlalchemy import func
from api.models.user_preference_models import UserPreference
from api.models.user_activity_models import UserActivity
from api.models.tag_models import Tag
from api.models.programs_tags_link import ProgramTagLink
from api.models.daily_log_models import DailyLog
from datetime import date, timedelta
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


@router.get("/test/{user_id}")
def test(session: SessionDep, user_id: int):
    since = date.today() - timedelta(days=7)

    row = session.exec(
        select(
            func.avg(DailyLog.stress),
            func.avg(DailyLog.sleep_score),
            func.avg(DailyLog.focus),
            func.avg(DailyLog.mood),
            func.avg(DailyLog.physical_activity)
        )
        .where(DailyLog.user_id == user_id)
        .where(DailyLog.date >= since)
    ).one()

    return {
        "stress": int(row[0] or 0),
        "sleep": int(row[1] or 0),
        "focus": int(row[2] or 0),
        "mood": int(row[3] or 0),
        "physical_activity": int(row[4] or 0),
    }