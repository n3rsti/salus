from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Program(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    duration_days: int
    description: str
    language: str

    days: List["ProgramDay"] = Relationship(back_populates="program", cascade_delete=True)


class ProgramRead(SQLModel):
    id: int
    name: str
    duration_days: int
    description: str
    language: str
    days: List["ProgramDayRead"] = []

class ProgramDay(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    day_number: int

    program_id: int | None = Field(default=None, foreign_key="program.id", ondelete="CASCADE")
    program: Program | None = Relationship(back_populates="days")

class ProgramDayRead(SQLModel):
    id: int
    description: str
    day_number: int
    program_id: int | None = None
