from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from api.models.daily_log_emotions_link import DailyLogEmotionLink

# This file contains models implementing: Emotions table


class EmotionBase(SQLModel):
    name: str
    icon: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("name cannot be empty or whitespace")
        return v

    @field_validator("icon")
    def validate_icon(cls, v):
        if v is not None and not v.strip():
            raise ValueError("icon cannot be empty or whitespace")
        return v


class Emotion(EmotionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    daily_logs: List["DailyLog"] = Relationship(
        back_populates="emotions", link_model=DailyLogEmotionLink
    )


class EmotionCreate(EmotionBase):
    pass


class EmotionUpdate(SQLModel):
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


class EmotionRead(EmotionBase):
    id: int


from api.models.daily_log_models import DailyLog

SQLModel.model_rebuild()
