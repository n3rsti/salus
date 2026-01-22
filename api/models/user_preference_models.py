from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

# This file contains models implementing: UserPreferences table


class UserPreferenceBase(SQLModel):
    mood: Optional[int] = Field(default=None)
    sleep: Optional[int] = Field(default=None)
    stress: Optional[int] = Field(default=None)
    focus: Optional[int] = Field(default=None)
    physical_activity: Optional[int] = Field(default=None)


class UserPreference(UserPreferenceBase, table=True):
    user_id: int = Field(primary_key=True, foreign_key="users.id")
    user: Optional["Users"] = Relationship()


class UserPreferenceCreate(UserPreferenceBase):
    pass


class UserPreferenceUpdate(SQLModel):
    mood: Optional[int] = None
    sleep: Optional[int] = None
    stress: Optional[int] = None
    focus: Optional[int] = None
    physical_activity: Optional[int] = None


class UserPreferenceRead(UserPreferenceBase):
    user_id: int


from api.models.user_models import Users

SQLModel.model_rebuild()
