from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from api.models.programs_tags_link import ProgramTagLink

# This file contains models implementing: Tags table


class TagBase(SQLModel):
    name: str
    icon: str

    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("name cannot be empty or whitespace")
        return v

    @field_validator("icon")
    def validate_icon(cls, v):
        if not v.strip():
            raise ValueError("icon cannot be empty or whitespace")
        return v


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    programs: List["Program"] = Relationship(
        back_populates="tags", link_model=ProgramTagLink
    )


class TagCreate(TagBase):
    pass


class TagUpdate(SQLModel):
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


class TagRead(TagBase):
    id: int


from api.models.program_models import Program

SQLModel.model_rebuild()
