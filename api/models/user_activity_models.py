from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from pydantic import model_validator

# This file contains models implementing: UserActivities table

class UserActivityBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    program_id: Optional[int] = Field(default=None, foreign_key="program.id")
    activity_id: Optional[int] = Field(default=None, foreign_key="activity.id")
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @model_validator(mode="after")
    def check_either_program_or_activity(self) -> "UserActivityBase":
        if (self.program_id is not None) == (self.activity_id is not None):
            raise ValueError("Exactly one of program_id or activity_id must be provided")
        return self


class UserActivity(UserActivityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional["Users"] = Relationship(back_populates="user_activities")
    program: Optional["Program"] = Relationship()
    activity: Optional["Activity"] = Relationship()


class UserActivityCreate(UserActivityBase):
    pass


class UserActivityUpdate(SQLModel):
    program_id: Optional[int] = None
    activity_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @model_validator(mode="after")
    def check_xor_update(self) -> "UserActivityUpdate":
        if self.program_id is not None and self.activity_id is not None:
            raise ValueError("Cannot set both program_id and activity_id simultaneously")
        return self


class UserActivityRead(UserActivityBase):
    id: int

from api.models.user_models import Users
from api.models.program_models import Program, Activity

SQLModel.model_rebuild()