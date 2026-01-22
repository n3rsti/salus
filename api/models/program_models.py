from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from api.models.program_day_activities_link import ProgramDayActivityLink

from sqlalchemy import Select, func, or_, Column, JSON
from pydantic import BaseModel, field_validator
from api.models.enums import Tag

# This file contains models implementing: Programs and ProgramDays tables


class ProgramBase(SQLModel):
    name: str
    duration_days: int
    description: str
    language: str
    image_url: str

    @field_validator("language")
    def validate_language(cls, v):
        allowed_languages = {
            "en",
            "pl",
            "hr",
            "el",
        }  # according to ISO 639-1 Language Code
        if v not in allowed_languages:
            raise ValueError(f"language must be one of {allowed_languages}")
        return v


class Program(ProgramBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="users.id", nullable=False)
    owner: Optional["Users"] = Relationship()

    days: List["ProgramDay"] = Relationship(
        back_populates="program", cascade_delete=True
    )

    tags: list[Tag] = Field(sa_column=Column(JSON, nullable=False, default=list))


class ProgramDayInput(SQLModel):
    description: str
    day_number: int
    activities_ids: List[int] = []


class ProgramCreate(ProgramBase):
    days: List[ProgramDayInput] = []
    tags: list[Tag] = []
    pass


class ProgramUpdate(SQLModel):
    name: Optional[str] = None
    duration_days: Optional[int] = None
    description: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[list[Tag]] = None
    days: List[ProgramDayInput] = []

    @field_validator("language")
    def validate_language(cls, v):
        if v is None:
            return v
        allowed_languages = {
            "en",
            "pl",
            "hr",
            "el",
        }  # according to ISO 639-1 Language Code
        if v not in allowed_languages:
            raise ValueError(f"language must be one of {allowed_languages}")
        return v


class ProgramRead(ProgramBase):
    id: int
    owner: "UsersRead"
    days: List["ProgramDayRead"] = []
    tags: list[Tag] = []
    average_rating: Optional[float] = None


class ProgramReadLight(ProgramBase):
    id: int
    owner: "UsersRead"
    tags: list[Tag] = []
    average_rating: Optional[float] = None


class ProgramFilters(BaseModel):
    search: Optional[str] = None
    limit: Optional[int] = None
    skip: Optional[int] = None
    user_id: Optional[int] = None

    def apply(self, query: Select) -> Select:
        if self.search:
            search_vector = func.to_tsvector("simple", func.coalesce(Program.name, ""))
            search_query = func.plainto_tsquery("simple", self.search)
            fts_match = search_vector.op("@@")(search_query)
            fuzzy_match = func.similarity(Program.name, self.search) > 0.3
            query = query.where(or_(fts_match, fuzzy_match))
            query = query.order_by(func.ts_rank(search_vector, search_query).desc())

        if self.limit:
            query = query.limit(self.limit)

        if self.user_id:
            query = query.where(Program.owner_id == self.user_id)

        if self.skip:
            query = query.offset(self.skip)

        return query


class ProgramDayBase(SQLModel):
    description: str
    day_number: int


class ProgramDay(ProgramDayBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: Optional[int] = Field(
        default=None, foreign_key="program.id", ondelete="CASCADE"
    )

    program: Optional["Program"] = Relationship(back_populates="days")
    activities: List["Activity"] = Relationship(
        back_populates="program_days", link_model=ProgramDayActivityLink
    )


class ProgramDayRead(ProgramDayBase):
    id: int
    program_id: int
    activities: List["ActivityRead"] = []


from api.models.activity_models import Activity, ActivityRead

# from api.models.tag_models import Tag, TagRead
from api.models.user_models import Users, UsersRead

SQLModel.model_rebuild()
