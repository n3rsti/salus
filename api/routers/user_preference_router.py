from ast import Dict
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from typing import Any, Optional

from api.database import SessionDep
from api.models.user_preference_models import (
    UserPreference,
    UserPreferenceRead,
    UserPreferenceCreate,
    UserPreferenceUpdate,
    UserPreferenceBase,
)
from api.security.auth import JwtPayload, get_current_user, verify_jwt_token

# This file contains API endpoints related to User Preferences

router = APIRouter(prefix="/api/user-preferences", tags=["UserPreferences"])


@router.get("/me", response_model=UserPreferenceRead)
def get_my_preferences(
    session: SessionDep, current_user: JwtPayload = Depends(get_current_user)
):
    statement = select(UserPreference).where(UserPreference.user_id == current_user.id)
    preference = session.exec(statement).first()

    if not preference:
        raise HTTPException(
            status_code=404, detail="Preferences not found for this user"
        )

    return preference


@router.post("", response_model=UserPreferenceRead)
def create_my_preferences(
    preference_in: UserPreferenceBase,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    existing = session.get(UserPreference, current_user.id)
    if existing:
        raise HTTPException(
            status_code=400, detail="Preferences already exist for this user"
        )

    preference = UserPreference.model_validate(
        preference_in, update={"user_id": current_user.id}
    )

    session.add(preference)
    session.commit()
    session.refresh(preference)
    return preference


@router.put("/me", response_model=UserPreferenceRead)
def update_my_preferences(
    preference_update: UserPreferenceUpdate,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    preference = session.get(UserPreference, current_user.id)

    if not preference:
        raise HTTPException(status_code=404, detail="Preferences not found")

    update_data = preference_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(preference, key, value)

    session.add(preference)
    session.commit()
    session.refresh(preference)
    return preference
