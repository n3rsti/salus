from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel
from api.models.activity_models import ActivityReadLight


class ActivityFeedItem(BaseModel):
    id: int
    program_id: Optional[int]
    program_day_id: Optional[int]
    start_date: datetime
    end_date: Optional[datetime]
    activity: Optional[ActivityReadLight]


class ProgramDayInfo(BaseModel):
    id: int
    day_number: int
    description: str
    activities: List[ActivityReadLight]


class ProgramInfo(BaseModel):
    id: int
    name: str
    description: str
    image_url: str
    owner_username: str
    days: List[ProgramDayInfo]
    user_activities: Dict[int, int]


class ActivitiesFeedResponse(BaseModel):
    activities: List[ActivityFeedItem]
    programs: List[ProgramInfo]
    limit: int
    offset: int
    has_more: bool
