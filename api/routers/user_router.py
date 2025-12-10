from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from api.database import SessionDep
from api.models.user_models import Users, UsersCreate, UsersRead, UsersUpdate, Role
from api.security.crypto import hash_password

# This file contains API endpoints related to Users (CRUD and role assignment)

router = APIRouter(prefix="/api/users", tags=["Users"])


# Users:
@router.post("", response_model=UsersRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UsersCreate, session: SessionDep):
    # check username uniqueness
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

    # validate role_id
    role = session.get(Role, data.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role_id",
        )

    # hash password
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
def list_users(session: SessionDep):
    users = session.exec(select(Users)).all()
    return users


@router.get("/{user_id}", response_model=UsersRead)
def get_user(user_id: int, session: SessionDep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UsersRead)
def update_user(user_id: int, data: UsersUpdate, session: SessionDep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # username change
    if data.username is not None:
        # check if username already used by another user
        existing = session.exec(
            select(Users).where(Users.username == data.username, Users.id != user_id)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )
        user.username = data.username

    # password change
    if data.password is not None:
        user.password = hash_password(data.password)

    if data.email is not None:
        email_owner = session.exec(
            select(Users).where(Users.email == data.email, Users.id != user_id)
        ).first()
        if email_owner:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        user.email = data.email

    # role change
    if data.role_id is not None:
        role = session.get(Role, data.role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role_id",
            )
        user.role_id = data.role_id

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(user)
    session.commit()
    return None
