from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator
from sqlalchemy import Select
from sqlmodel import Field, Relationship, SQLModel

# This file contains models implementing: UserActivities table


class UserActivityBase(SQLModel):
    program_id: Optional[int] = Field(default=None, foreign_key="program.id")
    activity_id: Optional[int] = Field(default=None, foreign_key="activity.id")
    program_day_id: Optional[int] = Field(default=None, foreign_key="programday.id")

    @model_validator(mode="after")
    def check_either_program_or_activity(self) -> "UserActivityBase":
        has_program = self.program_id is not None
        has_activity = self.activity_id is not None
        has_program_day = self.program_day_id is not None

        if not has_program and not has_activity:
            raise ValueError(
                "At least one of program_id or activity_id must be provided"
            )

        if has_program and has_activity and not has_program_day:
            raise ValueError(
                "program_day_id is required when both program_id and activity_id are set"
            )

        if has_program_day and not (has_program and has_activity):
            raise ValueError("program_day_id requires both program_id and activity_id")

        return self


class UserActivity(UserActivityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")

    user: Optional["Users"] = Relationship(back_populates="user_activities")
    program: Optional["Program"] = Relationship()
    activity: Optional["Activity"] = Relationship()
    start_date: datetime
    end_date: Optional[datetime] = None


class UserActivityCreate(UserActivityBase):
    pass


class UserActivityUpdate(SQLModel):
    end_date: Optional[datetime] = None


class UserActivityRead(UserActivityBase):
    id: int
    user_id: int
    start_date: datetime
    end_date: Optional[datetime]


class UserActivityFilters(BaseModel):
    limit: Optional[int] = None

    def apply(self, query: Select) -> Select:
        if self.limit:
            query = query.limit(self.limit)

        return query


from api.models.program_models import Activity, Program
from api.models.user_models import Users

SQLModel.model_rebuild()
