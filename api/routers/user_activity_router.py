from datetime import date
import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import delete, select, update

from api.database import SessionDep
from api.models.user_activity_models import (
    UserActivity,
    UserActivityCreate,
    UserActivityRead,
    UserActivityUpdate,
)
from api.security.auth import JwtPayload, get_current_user

router = APIRouter(prefix="/api/user-activities", tags=["UserActivities"])


@router.get("", response_model=List[UserActivityRead])
def get_user_activities(
    session: SessionDep, current_user: JwtPayload = Depends(get_current_user)
):
    statement = select(UserActivity).where(UserActivity.user_id == current_user.id)
    activities = session.exec(statement).all()
    return activities if activities else []


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
    user_activity_data["start_date"] = date.today()
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
