from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, update

from api.database import SessionDep
from api.models.trainer_request import (
    TrainerRequest,
    TrainerRequestCreate,
    TrainerRequestRead,
    TrainerRequestUpdate,
)
from api.security.auth import JwtPayload, get_current_user, is_admin


router = APIRouter(prefix="/api/requests", tags=["Requests"])


@router.post("", response_model=TrainerRequestRead)
def create_trainer_request(
    session: SessionDep,
    request_in: TrainerRequestCreate,
    current_user: JwtPayload = Depends(get_current_user),
):
    request_data = request_in.model_dump()
    request_data["user_id"] = current_user.id

    request = TrainerRequest.model_validate(request_data)

    session.add(request)
    session.commit()
    session.refresh(request)
    return request


@router.get("", response_model=list[TrainerRequestRead])
def get_trainer_requests(
    session: SessionDep, current_user: JwtPayload = Depends(get_current_user)
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized")

    requests = session.exec(select(TrainerRequest)).all()
    return requests if requests else []


def get_user_trainer_requests(
    session: SessionDep,
    user_id: int,
    current_user: JwtPayload = Depends(get_current_user),
):
    if not is_admin(current_user) and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    requests = session.exec(
        select(TrainerRequest).where(TrainerRequest.user_id == user_id)
    ).all()
    return requests if requests else []


@router.get("/{request_id}", response_model=TrainerRequestRead)
def get_trainer_request(
    session: SessionDep,
    request_id: int,
    current_user: JwtPayload = Depends(get_current_user),
):
    request = session.get(TrainerRequest, request_id)
    if not request:
        raise ValueError("Request not found")

    if not is_admin(current_user) and request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return request


@router.put("/{request_id}", response_model=TrainerRequestRead)
def update_trainer_request(
    session: SessionDep,
    request_id: int,
    request_update: TrainerRequestUpdate,
    current_user: JwtPayload = Depends(get_current_user),
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized")

    stmt = (
        update(TrainerRequest)
        .where(TrainerRequest.id == request_id)
        .values(**request_update.model_dump())
        .returning(TrainerRequest)
    )
    result = session.exec(stmt)
    session.commit()

    updated_request = result.scalar_one_or_none()
    if not updated_request:
        raise HTTPException(status_code=404, detail="Request not found")

    return updated_request
