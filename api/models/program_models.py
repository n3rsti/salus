from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from models.program_day_activities_link import ProgramDayActivityLink
from models.programs_tags_link import ProgramTagLink

# This file contains models implementing: Activities, ActivityMedia, Programs and ProgramDays tables 

class Program(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    duration_days: int
    description: str
    language: str
    image_url: str

    days: List["ProgramDay"] = Relationship(back_populates="program", cascade_delete=True)
    tags: list["Tag"] = Relationship(back_populates="programs", link_model=ProgramTagLink)

class ProgramDay(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    day_number: int

    program_id: int | None = Field(default=None, foreign_key="program.id", ondelete="CASCADE")
    program: Program | None = Relationship(back_populates="days")
    activities: list["Activity"] = Relationship(back_populates="program_days", link_model=ProgramDayActivityLink)

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

class ProgramRead(SQLModel):
    id: int
    name: str
    duration_days: int
    description: str
    language: str
    image_url: str
    days: List["ProgramDayRead"] = []
    tags: List["TagRead"] = []

class ProgramDayRead(SQLModel):
    id: int
    description: str
    day_number: int
    program_id: int | None = None
    activities: list["ActivityRead"] = []

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