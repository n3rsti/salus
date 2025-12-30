from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import delete, select, update

from api.database import SessionDep
from api.models.activity_plan_models import (
    ActivityPlan,
    ActivityPlanCreate,
    ActivityPlanRead,
    ActivityPlanUpdate,
)
from api.security.auth import JwtPayload, get_current_user

router = APIRouter(prefix="/api/activity-plans", tags=["ActivityPlans"])


@router.get("", response_model=List[ActivityPlanRead])
def get_activity_plans(
    session: SessionDep, current_user: JwtPayload = Depends(get_current_user)
):
    statement = select(ActivityPlan).where(ActivityPlan.user_id == current_user.id)
    plans = session.exec(statement).all()
    return plans if plans else []


@router.get("/{plan_id}", response_model=ActivityPlanRead)
def get_activity_plan(
    plan_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = select(ActivityPlan).where(
        (ActivityPlan.id == plan_id) & (ActivityPlan.user_id == current_user.id)
    )
    plan = session.exec(statement).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Activity plan not found")
    return plan


@router.post("", response_model=ActivityPlanRead)
def create_activity_plan(
    plan_in: ActivityPlanCreate,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    plan_data = plan_in.model_dump()
    plan_data["user_id"] = current_user.id
    plan = ActivityPlan.model_validate(plan_data)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.put("/{plan_id}", response_model=ActivityPlanRead)
def update_activity_plan(
    plan_id: int,
    plan_update: ActivityPlanUpdate,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    update_data = plan_update.model_dump(exclude_unset=True)
    statement = (
        update(ActivityPlan)
        .where((ActivityPlan.id == plan_id) & (ActivityPlan.user_id == current_user.id))
        .values(**update_data)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Activity plan not found")

    plan = session.get(ActivityPlan, plan_id)
    return plan


@router.delete("/{plan_id}")
def delete_activity_plan(
    plan_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = delete(ActivityPlan).where(
        (ActivityPlan.id == plan_id) & (ActivityPlan.user_id == current_user.id)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Activity plan not found")

    return {"ok": True}
