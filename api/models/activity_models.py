from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from api.models.program_day_activities_link import ProgramDayActivityLink

# This file contains models implementing: Activities and ActivitesMedia tables


class ActivityBase(SQLModel):
    name: str
    duration_minutes: int
    description: str
    difficulty: int
    image_url: str

    @field_validator("difficulty")
    def validate_difficulty(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("difficulty must be between 1 and 5")
        return v


class Activity(ActivityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="users.id", nullable=False)
    owner: Optional["Users"] = Relationship()

    media: List["ActivityMedia"] = Relationship(
        back_populates="activity", cascade_delete=True
    )
    program_days: List["ProgramDay"] = Relationship(
        back_populates="activities", link_model=ProgramDayActivityLink
    )


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(SQLModel):
    name: Optional[str] = None
    duration_minutes: Optional[int] = None
    description: Optional[str] = None
    difficulty: Optional[int] = None
    image_url: Optional[str] = None

    @field_validator("difficulty")
    def validate_difficulty(cls, v):
        if v is None:
            return v
        if not (1 <= v <= 5):
            raise ValueError("difficulty must be between 1 and 5")
        return v


class ActivityRead(ActivityBase):
    id: int
    owner: "UsersRead"
    media: List["ActivityMediaRead"] = []


class ActivityMediaBase(SQLModel):
    url: str
    type: str

    @field_validator("type")
    def validate_type(cls, v):
        allowed_types = {"image", "video", "audio", "article"}
        if v not in allowed_types:
            raise ValueError(f"type must be one of {allowed_types}")
        return v


class ActivityMedia(ActivityMediaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: Optional[int] = Field(
        default=None, foreign_key="activity.id", ondelete="CASCADE"
    )
    activity: Optional["Activity"] = Relationship(back_populates="media")


class ActivityMediaCreate(ActivityMediaBase):
    activity_id: int


class ActivityMediaUpdate(SQLModel):
    url: Optional[str] = None
    type: Optional[str] = None
    activity_id: Optional[int] = None

    @field_validator("type")
    def validate_type(cls, v):
        if v is None:
            return v
        allowed_types = {"image", "video", "audio", "article"}
        if v not in allowed_types:
            raise ValueError(f"type must be one of {allowed_types}")
        return v


class ActivityMediaRead(ActivityMediaBase):
    id: int
    activity_id: int


from api.models.program_models import ProgramDay
from api.models.user_models import Users, UsersRead

SQLModel.model_rebuild()
