from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Activity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    duration_minutes: int
    description: str
    difficulty: int
    media: List["ActivityMedia"] = Relationship(back_populates="activity", cascade_delete=True, )

class ActivityMedia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    type: str

    activity_id: int | None = Field(default=None, foreign_key="activity.id", ondelete="CASCADE")
    activity: Activity | None = Relationship(back_populates="media")

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
    media: List[ActivityMediaRead] = []


