from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List

from api.database import SessionDep
from api.models.user_activity_models import (
    UserActivity, 
    UserActivityRead, 
    UserActivityCreate, 
    UserActivityUpdate
)
from api.models.user_models import Users
from api.models.program_models import Program, Activity

# This file contains API endpoints related to User Activities

router = APIRouter(prefix="/api/user-activities", tags=["UserActivities"])


@router.get("", response_model=List[UserActivityRead])
def get_user_activities(session: SessionDep):
    activities = session.exec(select(UserActivity)).all()
    return activities if activities else []


@router.get("/{ua_id}", response_model=UserActivityRead)
def get_user_activity(ua_id: int, session: SessionDep):
    user_activity = session.get(UserActivity, ua_id)
    if not user_activity:
        raise HTTPException(status_code=404, detail="User activity assignment not found")
    return user_activity


@router.post("", response_model=UserActivityRead)
def create_user_activity(ua_in: UserActivityCreate, session: SessionDep):
    if not session.get(Users, ua_in.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if ua_in.program_id:
        if not session.get(Program, ua_in.program_id):
            raise HTTPException(status_code=404, detail="Program not found")
    elif ua_in.activity_id:
        if not session.get(Activity, ua_in.activity_id):
            raise HTTPException(status_code=404, detail="Activity not found")

    user_activity = UserActivity.model_validate(ua_in)
    session.add(user_activity)
    session.commit()
    session.refresh(user_activity)
    return user_activity


@router.put("/{ua_id}", response_model=UserActivityRead)
def update_user_activity(
    ua_id: int, 
    ua_update: UserActivityUpdate, 
    session: SessionDep
):
    user_activity = session.get(UserActivity, ua_id)
    if not user_activity:
        raise HTTPException(status_code=404, detail="User activity assignment not found")

    update_data = ua_update.model_dump(exclude_unset=True)

    if "user_id" in update_data:
        if not session.get(Users, update_data["user_id"]):
            raise HTTPException(status_code=404, detail="New user not found")
    
    if "program_id" in update_data and update_data["program_id"] is not None:
        if not session.get(Program, update_data["program_id"]):
            raise HTTPException(status_code=404, detail="New program not found")
            
    if "activity_id" in update_data and update_data["activity_id"] is not None:
        if not session.get(Activity, update_data["activity_id"]):
            raise HTTPException(status_code=404, detail="New activity not found")

    for key, value in update_data.items():
        setattr(user_activity, key, value)

    session.add(user_activity)
    session.commit()
    session.refresh(user_activity)
    return user_activity


@router.delete("/{ua_id}")
def delete_user_activity(ua_id: int, session: SessionDep):
    user_activity = session.get(UserActivity, ua_id)
    if not user_activity:
        raise HTTPException(status_code=404, detail="User activity assignment not found")
    
    session.delete(user_activity)
    session.commit()
    return {"ok": True}