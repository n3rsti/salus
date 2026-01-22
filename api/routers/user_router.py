from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import delete, select

from api.database import SessionDep
from api.models.enums import Role
from api.models.trainer_request import TrainerRequestRead
from api.models.user_models import Users, UsersCreate, UsersRead, UsersUpdate
from api.routers.trainer_router import get_user_trainer_requests
from api.security.auth import JwtPayload, get_current_user, is_admin, is_super_admin
from api.security.crypto import hash_password

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("", response_model=UsersRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UsersCreate, session: SessionDep):
    existing = session.exec(
        select(Users).where(Users.username == data.username)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    if data.email is not None:
        email_owner = session.exec(
            select(Users).where(Users.email == data.email)
        ).first()
        if email_owner:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

    password_hash = hash_password(data.password)

    user = Users(
        username=data.username,
        email=data.email,
        role_id=data.role_id,
        password=password_hash,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("", response_model=list[UsersRead])
def list_users(
    session: SessionDep, current_user: JwtPayload = Depends(get_current_user)
):
    users = session.exec(select(Users)).all()
    return users


@router.get("/{user_id}", response_model=UsersRead)
def get_user(
    user_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UsersRead)
def update_user(
    user_id: int,
    data: UsersUpdate,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    if not is_admin(current_user) and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    user_data = data.model_dump(exclude_unset=True)

    if data.password is not None:
        user_data["password"] = hash_password(data.password)

    if data.role_id is not None:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
            )

        if data.role_id not in [Role.USER, Role.TRAINER] and not is_super_admin(
            current_user
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
            )
        user_data["role_id"] = data.role_id

    statement = (
        update(Users).where(Users.id == user_id).values(**user_data).returning(Users)
    )
    result = session.exec(statement)
    session.commit()

    updated_user = result.scalar_one_or_none()
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = delete(Users).where(Users.id == user_id)
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return None


@router.get("/{user_id}/requests", response_model=list[TrainerRequestRead])
def get_user_requests(
    user_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    return get_user_trainer_requests(session, user_id, current_user)
