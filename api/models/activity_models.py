from typing import List, Optional
from fastapi import Query
from sqlalchemy import Select, func, or_
from sqlmodel import SQLModel, Field, Relationship, col
from pydantic import BaseModel, field_validator
from api.models.program_day_activities_link import ProgramDayActivityLink

# This file contains models implementing: Activities and ActivitesMedia tables


class ActivityBase(SQLModel):
    name: str
    duration_minutes: int
    description: str
    difficulty: int

    @field_validator("difficulty")
    def validate_difficulty(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("difficulty must be between 1 and 5")
        return v


class Activity(ActivityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="users.id", nullable=False)
    owner: Optional["Users"] = Relationship()

    image_url: str

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
    image_url: str


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


class ActivityFilters(BaseModel):
    search: Optional[str] = None
    limit: Optional[int] = None

    def apply(self, query: Select) -> Select:
        if self.search:
            search_vector = func.to_tsvector(
                "simple",
                func.coalesce(Activity.name, "")
                + " "
                + func.coalesce(Activity.description, ""),
            )
            search_query = func.plainto_tsquery("simple", self.search)
            fts_match = search_vector.op("@@")(search_query)

            fuzzy_match = func.similarity(Activity.name, self.search) > 0.3

            query = query.where(or_(fts_match, fuzzy_match))

            query = query.order_by(func.ts_rank(search_vector, search_query).desc())

        if self.limit:
            query = query.limit(self.limit)

        return query


from api.models.program_models import ProgramDay
from api.models.user_models import Users, UsersRead

SQLModel.model_rebuild()
