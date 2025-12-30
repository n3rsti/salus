from datetime import date
from typing import List, Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from api.models.daily_log_emotions_link import DailyLogEmotionLink

# This file contains models implementing: DailyLogs table


class DailyLogBase(SQLModel):
    date: date
    mood: Optional[int] = None
    sleep_score: Optional[int] = None
    stress: Optional[int] = None
    focus: Optional[int] = None
    physical_activity: Optional[int] = None
    alcohol_intake: Optional[int] = None
    notes: Optional[str] = None


class DailyLog(DailyLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id", nullable=False)
    user: Optional["Users"] = Relationship()
    emotions: List["Emotion"] = Relationship(
        back_populates="daily_logs", link_model=DailyLogEmotionLink
    )


class DailyLogCreate(DailyLogBase):
    pass


class DailyLogUpdate(SQLModel):
    date: Optional[date] = None
    mood: Optional[int] = None
    sleep_score: Optional[int] = None
    stress: Optional[int] = None
    focus: Optional[int] = None
    physical_activity: Optional[int] = None
    alcohol_intake: Optional[int] = None
    notes: Optional[str] = None


class DailyLogRead(DailyLogBase):
    id: int
    emotions: List["EmotionRead"] = []
    user: "UsersRead"


from api.models.emotion_models import Emotion, EmotionRead
from api.models.user_models import Users, UsersRead

SQLModel.model_rebuild()
