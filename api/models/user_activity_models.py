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

    @model_validator(mode="after")
    def check_either_program_or_activity(self) -> "UserActivityBase":
        if (self.program_id is None) and (self.activity_id is None):
            raise ValueError(
                "At least one of program_id or activity_id must be provided"
            )
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
