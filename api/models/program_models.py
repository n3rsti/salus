from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from models.program_day_activities_link import ProgramDayActivityLink
from models.programs_tags_link import ProgramTagLink
from pydantic import field_validator

# This file contains models implementing: Activities, ActivityMedia, Programs and ProgramDays tables 

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

    media: List["ActivityMedia"] = Relationship(back_populates="activity",cascade_delete=True)
    program_days: List["ProgramDay"] = Relationship(back_populates="activities",link_model=ProgramDayActivityLink)

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
    activity_id: Optional[int] = Field(default=None, foreign_key="activity.id", ondelete="CASCADE")
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

# class Tag(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     icon: str

#     programs: list["Program"] = Relationship(back_populates="tags", link_model=ProgramTagLink)

class TagBase(SQLModel):
    name: str
    icon: str

    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("name cannot be empty or whitespace")
        return v

    @field_validator("icon")
    def validate_icon(cls, v):
        if not v.strip():
            raise ValueError("icon cannot be empty or whitespace")
        return v

class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    programs: List["Program"] = Relationship(back_populates="tags",link_model=ProgramTagLink)

class TagCreate(TagBase):
    pass

class TagUpdate(SQLModel):
    name: Optional[str] = None
    icon: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError("name cannot be empty or whitespace")
        return v

    @field_validator("icon")
    def validate_icon(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError("icon cannot be empty or whitespace")
        return v

class TagRead(TagBase):
    id: int

# class TagRead(SQLModel):
#     id: int
#     name: str
#     icon: str