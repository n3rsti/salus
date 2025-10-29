from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

# This file contains model implementing: ProgramTags table which links Programs and Tags 

class ProgramTagLink(SQLModel, table=True):
    program_id: int | None = Field(default=None, foreign_key="program.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
