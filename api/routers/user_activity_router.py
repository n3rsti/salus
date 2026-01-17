from datetime import date, datetime
import time
from typing import List, Optional, Tuple, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import delete, func, select, update

from api.database import SessionDep
from api.models.activity_models import Activity, ActivityReadLight
from api.models.program_models import Program, ProgramDay
from api.models.user_activities_response_models import (
    ActivitiesFeedResponse,
    ActivityFeedItem,
    ProgramDayInfo,
    ProgramInfo,
)
from api.models.user_activity_models import (
    UserActivity,
    UserActivityCreate,
    UserActivityRead,
    UserActivityUpdate,
)
from api.models.user_models import Users
from api.security.auth import JwtPayload, get_current_user

router = APIRouter(prefix="/api/user-activities", tags=["UserActivities"])


@router.get("", response_model=List[UserActivityRead])
def get_user_activities(
    session: SessionDep,
    limit: Optional[int] = None,
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = select(UserActivity).where(UserActivity.user_id == current_user.id)

    if limit:
        statement = statement.limit(limit)

    activities = session.exec(statement).all()
    return activities if activities else []


def build_feed_items(
    activities_result: List[Tuple], program_ids: set
) -> List[ActivityFeedItem]:
    items = []
    for user_activity, activity, owner_username in activities_result:
        if user_activity.program_id:
            program_ids.add(user_activity.program_id)

        items.append(
            ActivityFeedItem(
                id=user_activity.id,
                program_id=user_activity.program_id,
                start_date=user_activity.start_date,
                end_date=user_activity.end_date,
                activity=(
                    ActivityReadLight(
                        id=activity.id,
                        owner_id=activity.owner_id,
                        owner_username=owner_username,
                        name=activity.name,
                        description=activity.description,
                        duration_minutes=activity.duration_minutes,
                        image_url=activity.image_url,
                        difficulty=activity.difficulty,
                        tags=activity.tags,
                    )
                    if activity
                    else None
                ),
            )
        )
    return items


def build_programs(programs_result: List[Tuple]) -> Dict[int, ProgramInfo]:
    programs = {}
    days_cache = {}

    for program, day, activity, owner_username, owner in programs_result:
        if program.id not in programs:
            programs[program.id] = ProgramInfo(
                id=program.id,
                name=program.name,
                description=program.description,
                image_url=program.image_url,
                owner_username=owner_username,
                days=[],
                user_activities={},
            )

        day_key = (program.id, day.id)
        if day_key not in days_cache:
            day_info = ProgramDayInfo(
                day_number=day.day_number,
                description=day.description,
                activities=[],
            )
            days_cache[day_key] = day_info
            programs[program.id].days.append(day_info)

        days_cache[day_key].activities.append(
            ActivityReadLight(
                id=activity.id,
                owner_id=activity.owner_id,
                owner_username=owner_username,
                name=activity.name,
                description=activity.description,
                duration_minutes=activity.duration_minutes,
                image_url=activity.image_url,
                difficulty=activity.difficulty,
                tags=activity.tags,
            )
        )

    return programs


def add_user_activities(
    programs: Dict[int, ProgramInfo],
    user_activities: List[UserActivity],
) -> None:
    for ua in user_activities:
        if ua.activity_id and ua.program_id in programs:
            programs[ua.program_id].user_activities[ua.activity_id] = ua.id


@router.get("/me/activities", response_model=ActivitiesFeedResponse)
def get_my_activities(
    session: SessionDep,
    limit: int = 50,
    offset: int = 0,
    current_user: JwtPayload = Depends(get_current_user),
):
    activities_result = session.exec(
        select(UserActivity, Activity, Users.username)
        .outerjoin(Activity, UserActivity.activity_id == Activity.id)
        .outerjoin(Users, Activity.owner_id == Users.id)
        .where(UserActivity.user_id == current_user.id)
        .order_by(UserActivity.start_date.desc())
        .limit(limit)
        .offset(offset)
    ).all()

    program_ids = set()
    feed_items = build_feed_items(activities_result, program_ids)

    total = session.exec(
        select(func.count())
        .select_from(UserActivity)
        .where(UserActivity.user_id == current_user.id)
    ).one()

    if not program_ids:
        return ActivitiesFeedResponse(
            activities=feed_items,
            programs=[],
            limit=limit,
            offset=offset,
            has_more=(offset + limit) < total,
        )

    programs_result = session.exec(
        select(Program, ProgramDay, Activity, Users.username, Users)
        .join(ProgramDay, Program.id == ProgramDay.program_id)
        .join(ProgramDay.activities)
        .join(Users, Program.owner_id == Users.id)
        .where(Program.id.in_(list(program_ids)))
        .order_by(Program.id, ProgramDay.day_number, Activity.id)
    ).all()

    user_activities = session.exec(
        select(UserActivity).where(
            UserActivity.user_id == current_user.id,
            UserActivity.program_id.in_(list(program_ids)),
        )
    ).all()

    programs = build_programs(programs_result)
    add_user_activities(programs, user_activities)

    return ActivitiesFeedResponse(
        activities=feed_items,
        programs=list(programs.values()),
        limit=limit,
        offset=offset,
        has_more=(offset + limit) < total,
    )


@router.get("/{ua_id}", response_model=UserActivityRead)
def get_user_activity(
    ua_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = select(UserActivity).where(
        (UserActivity.id == ua_id) & (UserActivity.user_id == current_user.id)
    )
    user_activity = session.exec(statement).first()
    if not user_activity:
        raise HTTPException(
            status_code=404, detail="User activity assignment not found"
        )
    return user_activity


@router.post("", response_model=UserActivityRead)
def create_user_activity(
    ua_in: UserActivityCreate,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    user_activity_data = ua_in.model_dump()
    user_activity_data["user_id"] = current_user.id
    user_activity_data["start_date"] = datetime.now()
    user_activity = UserActivity.model_validate(user_activity_data)

    session.add(user_activity)
    session.commit()
    session.refresh(user_activity)
    return user_activity


@router.post("/{ua_id}/complete", status_code=204)
def complete_user_activity(
    ua_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    # set end_date to today
    statement = (
        update(UserActivity)
        .where((UserActivity.id == ua_id) & (UserActivity.user_id == current_user.id))
        .values(end_date=date.today())
    )

    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404, detail="User activity assignment not found"
        )


@router.delete("/{ua_id}")
def delete_user_activity(
    ua_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = delete(UserActivity).where(
        (UserActivity.id == ua_id) & (UserActivity.user_id == current_user.id)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404, detail="User activity assignment not found"
        )

    return {"ok": True}
