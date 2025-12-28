from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# This file contains models implementing: ActivityPlan table

class ActivityPlanBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    activity_id: int = Field(foreign_key="activity.id")
    time: Optional[datetime] = None


class ActivityPlan(ActivityPlanBase, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional["Users"] = Relationship(back_populates="activity_plans")
    activity: Optional["Activity"] = Relationship()


class ActivityPlanCreate(ActivityPlanBase):
    pass


class ActivityPlanUpdate(SQLModel):
    user_id: Optional[int] = None
    activity_id: Optional[int] = None
    time: Optional[datetime] = None


class ActivityPlanRead(ActivityPlanBase):
    id: int

from api.models.user_models import Users
from api.models.activity_models import Activity
SQLModel.model_rebuild()