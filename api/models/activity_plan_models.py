from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

# This file contains models implementing: ActivityPlan table


class ActivityPlanBase(SQLModel):
    activity_id: int = Field(foreign_key="activity.id")
    time: Optional[datetime] = None


class ActivityPlan(ActivityPlanBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")

    user: Optional["Users"] = Relationship(back_populates="activity_plans")
    activity: Optional["Activity"] = Relationship()


class ActivityPlanCreate(ActivityPlanBase):
    pass


class ActivityPlanUpdate(SQLModel):
    activity_id: Optional[int] = None
    time: Optional[datetime] = None


class ActivityPlanRead(ActivityPlanBase):
    id: int
    user_id: int


from api.models.activity_models import Activity
from api.models.user_models import Users

SQLModel.model_rebuild()
