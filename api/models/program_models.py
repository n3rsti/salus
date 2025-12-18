from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from api.models.program_day_activities_link import ProgramDayActivityLink
from api.models.programs_tags_link import ProgramTagLink
from pydantic import field_validator

# This file contains models implementing: Programs and ProgramDays tables


class ProgramBase(SQLModel):
    name: str
    duration_days: int
    description: str
    language: str
    image_url: str

    @field_validator("language")
    def validate_language(cls, v):
        allowed_languages = {
            "en",
            "pl",
            "hr",
            "el",
        }  # according to ISO 639-1 Language Code
        if v not in allowed_languages:
            raise ValueError(f"language must be one of {allowed_languages}")
        return v


class Program(ProgramBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="users.id", nullable=False)
    owner: Optional["Users"] = Relationship()

    days: List["ProgramDay"] = Relationship(
        back_populates="program", cascade_delete=True
    )
    tags: List["Tag"] = Relationship(
        back_populates="programs", link_model=ProgramTagLink
    )


class ProgramDayInput(SQLModel):
    description: str
    day_number: int
    activities_ids: List[int] = []


class ProgramCreate(ProgramBase):
    days: List[ProgramDayInput] = []
    pass


class ProgramUpdate(SQLModel):
    name: Optional[str] = None
    duration_days: Optional[int] = None
    description: Optional[str] = None
    language: Optional[str] = None
    image_url: Optional[str] = None
    days: List[ProgramDayInput] = []

    @field_validator("language")
    def validate_language(cls, v):
        if v is None:
            return v
        allowed_languages = {
            "en",
            "pl",
            "hr",
            "el",
        }  # according to ISO 639-1 Language Code
        if v not in allowed_languages:
            raise ValueError(f"language must be one of {allowed_languages}")
        return v


class ProgramRead(ProgramBase):
    id: int
    days: List["ProgramDayRead"] = []
    tags: List["TagRead"] = []


class ProgramDayBase(SQLModel):
    description: str
    day_number: int


class ProgramDay(ProgramDayBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: Optional[int] = Field(
        default=None, foreign_key="program.id", ondelete="CASCADE"
    )

    program: Optional["Program"] = Relationship(back_populates="days")
    activities: List["Activity"] = Relationship(
        back_populates="program_days", link_model=ProgramDayActivityLink
    )


class ProgramDayRead(ProgramDayBase):
    id: int
    program_id: int
    activities: List["ActivityRead"] = []


from api.models.activity_models import Activity, ActivityRead
from api.models.tag_models import Tag, TagRead
from api.models.user_models import Users
SQLModel.model_rebuild()