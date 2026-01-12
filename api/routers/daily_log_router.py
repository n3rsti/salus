from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import delete, select, update

from api.database import SessionDep
from api.models.daily_log_models import (
    DailyLog,
    DailyLogCreate,
    DailyLogRead,
    DailyLogUpdate,
)
from api.security.auth import JwtPayload, get_current_user

router = APIRouter(prefix="/api/daily-logs", tags=["DailyLogs"])


@router.get("", response_model=List[DailyLogRead])
def get_daily_logs(
    session: SessionDep, current_user: JwtPayload = Depends(get_current_user)
):
    statement = select(DailyLog).where(DailyLog.user_id == current_user.id)
    logs = session.exec(statement).all()
    return logs if logs else []


@router.get("/{log_id}", response_model=DailyLogRead)
def get_daily_log(
    log_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = select(DailyLog).where(
        (DailyLog.id == log_id) & (DailyLog.user_id == current_user.id)
    )
    log = session.exec(statement).first()

    if not log:
        raise HTTPException(status_code=404, detail="Daily log not found")

    return log


@router.post("", response_model=DailyLogRead)
def create_daily_log(
    log_in: DailyLogCreate,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    log_data = log_in.model_dump()
    log_data["user_id"] = current_user.id

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
    current_user: JwtPayload = Depends(get_current_user),
):
    update_data = log_update.model_dump(exclude_unset=True)
    statement = (
        update(DailyLog)
        .where((DailyLog.id == log_id) & (DailyLog.user_id == current_user.id))
        .values(**update_data)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Daily log not found")

    log = session.get(DailyLog, log_id)
    return log


@router.delete("/{log_id}")
def delete_daily_log(
    session: SessionDep,
    log_id: int,
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = delete(DailyLog).where(
        (DailyLog.id == log_id) & (DailyLog.user_id == current_user.id)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Daily log not found")

    return {"ok": True}
