from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

# This file contains model implementing: DailyLogEmoyions table which links DailyLogs and Emotions

class DailyLogEmotionLink(SQLModel, table=True):
    daily_log_id: int | None = Field(
        default=None, foreign_key="dailylog.id", primary_key=True, ondelete="CASCADE"
    )
    emotion_id: int | None = Field(
        default=None, foreign_key="emotion.id", primary_key=True
    )