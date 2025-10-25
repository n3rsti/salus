from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

# This file contains model implementing: ProgramDaysActivities table which links Activities and ProgramDays 

class ProgramDayActivityLink(SQLModel, table=True):
    program_day_id: int | None = Field(default=None, foreign_key="programday.id", primary_key=True)
    activity_id: int | None = Field(default=None, foreign_key="activity.id", primary_key=True)
