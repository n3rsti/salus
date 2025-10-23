from sqlmodel import SQLModel, Field

class Activity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    duration_minutes: int
    description: str
    difficulty: int

class ActivityMedia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    type: str
    activity_id: int = Field(foreign_key="activity.id")