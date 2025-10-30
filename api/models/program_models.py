from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from models.program_day_activities_link import ProgramDayActivityLink
from models.programs_tags_link import ProgramTagLink
from pydantic import field_validator

# This file contains models implementing: Activities, ActivityMedia, Programs and ProgramDays tables 

# class Program(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     duration_days: int
#     description: str
#     language: str
#     image_url: str

#     days: List["ProgramDay"] = Relationship(back_populates="program", cascade_delete=True)
#     tags: list["Tag"] = Relationship(back_populates="programs", link_model=ProgramTagLink)

class ProgramBase(SQLModel):
    name: str
    duration_days: int
    description: str
    language: str
    image_url: str

    @field_validator("language")
    def validate_language(cls, v):
        allowed_languages = {"en", "pl", "hr", "el"} #according to ISO 639-1 Language Code
        if v not in allowed_languages:
            raise ValueError(f"language must be one of {allowed_languages}")
        return v

class Program(ProgramBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    days: List["ProgramDay"] = Relationship(back_populates="program", cascade_delete=True)
    tags: List["Tag"] = Relationship(back_populates="programs", link_model=ProgramTagLink)

class ProgramCreate(ProgramBase):
    pass

class ProgramUpdate(SQLModel):
    name: Optional[str] = None
    duration_days: Optional[int] = None
    description: Optional[str] = None
    language: Optional[str] = None
    image_url: Optional[str] = None

    @field_validator("language")
    def validate_language(cls, v):
        if v is None:
            return v
        allowed_languages = {"en", "pl", "hr", "el"} #according to ISO 639-1 Language Code
        if v not in allowed_languages:
            raise ValueError(f"language must be one of {allowed_languages}")
        return v

class ProgramRead(ProgramBase):
    id: int
    days: List["ProgramDayRead"] = []
    tags: List["TagRead"] = []

# class ProgramDay(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     description: str
#     day_number: int

#     program_id: int | None = Field(default=None, foreign_key="program.id", ondelete="CASCADE")
#     program: Program | None = Relationship(back_populates="days")
#     activities: list["Activity"] = Relationship(back_populates="program_days", link_model=ProgramDayActivityLink)

class ProgramDayBase(SQLModel):
    description: str
    day_number: int

class ProgramDay(ProgramDayBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: Optional[int] = Field(default=None, foreign_key="program.id", ondelete="CASCADE")

    program: Optional["Program"] = Relationship(back_populates="days")
    activities: List["Activity"] = Relationship(back_populates="program_days",link_model=ProgramDayActivityLink)

class ProgramDayCreate(ProgramDayBase):
    program_id: int

class ProgramDayUpdate(SQLModel):
    description: Optional[str] = None
    day_number: Optional[int] = None
    program_id: Optional[int] = None

class ProgramDayRead(ProgramDayBase):
    id: int
    program_id: int
    activities: List["ActivityRead"] = []
#-----------------------------
class Activity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    duration_minutes: int
    description: str
    difficulty: int
    image_url: str
    media: List["ActivityMedia"] = Relationship(back_populates="activity", cascade_delete=True)

    program_days: list["ProgramDay"] = Relationship(back_populates="activities", link_model=ProgramDayActivityLink)

class ActivityMedia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    type: str

    activity_id: int | None = Field(default=None, foreign_key="activity.id", ondelete="CASCADE")
    activity: Activity | None = Relationship(back_populates="media")

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    icon: str

    programs: list["Program"] = Relationship(back_populates="tags", link_model=ProgramTagLink)

##### Read Models #####

# class ProgramRead(SQLModel):
#     id: int
#     name: str
#     duration_days: int
#     description: str
#     language: str
#     image_url: str
#     days: List["ProgramDayRead"] = []
#     tags: List["TagRead"] = []

# class ProgramDayRead(SQLModel):
#     id: int
#     description: str
#     day_number: int
#     program_id: int | None = None
#     activities: list["ActivityRead"] = []

class ActivityMediaRead(SQLModel):
    id: int
    url: str
    type: str
    activity_id: int | None = None

class ActivityRead(SQLModel):
    id: int
    name: str
    duration_minutes: int
    description: str
    difficulty: int
    image_url: str
    media: List[ActivityMediaRead] = []

class TagRead(SQLModel):
    id: int
    name: str
    icon: str