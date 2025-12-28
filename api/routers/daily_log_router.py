from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from typing import List

from api.database import SessionDep
from api.models.daily_log_models import (
    DailyLog, 
    DailyLogRead, 
    DailyLogCreate, 
    DailyLogUpdate
)
from api.security.auth import get_current_user

# This file contains API endpoints related to DailyLogs with User Ownership

router = APIRouter(prefix="/api/daily-logs", tags=["DailyLogs"])

@router.get("", response_model=List[DailyLogRead])
def get_daily_logs(
    session: SessionDep, 
    current_user: int = Depends(get_current_user)
):
    statement = select(DailyLog).where(DailyLog.user_id == current_user)
    logs = session.exec(statement).all()
    return logs if logs else []


@router.get("/{log_id}", response_model=DailyLogRead)
def get_daily_log(
    log_id: int, 
    session: SessionDep, 
    current_user: int = Depends(get_current_user)
):
    log = session.get(DailyLog, log_id)

    if not log:
        raise HTTPException(status_code=404, detail="Daily log not found")

    if log.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions to view this log")

    return log


@router.post("", response_model=DailyLogRead)
def create_daily_log(
    log_in: DailyLogCreate, 
    session: SessionDep, 
    current_user: int = Depends(get_current_user)
):
    log_data = log_in.model_dump()
    log_data["user_id"] = current_user
    
    log = DailyLog.model_validate(log_data)
    session.add(log)
    session.commit()
    session.refresh(log)
    return log


@router.put("/{log_id}", response_model=DailyLogRead)
def update_daily_log(
    session: SessionDep, 
    log_id: int, 
    log_update: DailyLogUpdate,
    current_user: int = Depends(get_current_user)
):
    log = session.get(DailyLog, log_id)

    if not log:
        raise HTTPException(status_code=404, detail="Daily log not found")

    if log.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions to edit this log")

    update_data = log_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(log, key, value)

    session.add(log)
    session.commit()
    session.refresh(log)
    return log


@router.delete("/{log_id}")
def delete_daily_log(
    session: SessionDep, 
    log_id: int,
    current_user: int = Depends(get_current_user)
):
    log = session.get(DailyLog, log_id)
    
    if not log:
        raise HTTPException(status_code=404, detail="Daily log not found")

    if log.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete this log")
    
    session.delete(log)
    session.commit()
    return {"ok": True}