from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List

from api.database import SessionDep
from api.models.activity_plan_models import (
    ActivityPlan, 
    ActivityPlanRead, 
    ActivityPlanCreate, 
    ActivityPlanUpdate
)
from api.models.user_models import Users
from api.models.activity_models import Activity

# This file contains API endpoints related to Activity Plans

router = APIRouter(prefix="/api/activity-plans", tags=["ActivityPlans"])


@router.get("", response_model=List[ActivityPlanRead])
def get_activity_plans(session: SessionDep):
    plans = session.exec(select(ActivityPlan)).all()
    return plans if plans else []


@router.get("/{plan_id}", response_model=ActivityPlanRead)
def get_activity_plan(plan_id: int, session: SessionDep):
    plan = session.get(ActivityPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Activity plan not found")
    return plan


@router.post("", response_model=ActivityPlanRead)
def create_activity_plan(plan_in: ActivityPlanCreate, session: SessionDep):
    user = session.get(Users, plan_in.user_id)
    activity = session.get(Activity, plan_in.activity_id)

    if not user or not activity:
        raise HTTPException(
            status_code=404, 
            detail="User or Activity linked to the plan not found"
        )

    plan = ActivityPlan.model_validate(plan_in)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.put("/{plan_id}", response_model=ActivityPlanRead)
def update_activity_plan(
    plan_id: int, 
    plan_update: ActivityPlanUpdate, 
    session: SessionDep
):
    plan = session.get(ActivityPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Activity plan not found")

    update_data = plan_update.model_dump(exclude_unset=True)

    if "user_id" in update_data:
        if not session.get(Users, update_data["user_id"]):
            raise HTTPException(status_code=404, detail="New user not found")
    
    if "activity_id" in update_data:
        if not session.get(Activity, update_data["activity_id"]):
            raise HTTPException(status_code=404, detail="New activity not found")

    for key, value in update_data.items():
        setattr(plan, key, value)

    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.delete("/{plan_id}")
def delete_activity_plan(plan_id: int, session: SessionDep):
    plan = session.get(ActivityPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Activity plan not found")
    
    session.delete(plan)
    session.commit()
    return {"ok": True}