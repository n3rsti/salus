from datetime import datetime
from typing import Optional
from sqlmodel import Field, Index, Relationship, SQLModel
from api.models.user_models import Users, UsersRead


class TrainerRequestBase(SQLModel):
    description: str


class TrainerRequest(TrainerRequestBase, table=True):
    __table_args__ = (
        Index(
            "ix_user_unresolved",
            "user_id",
            unique=True,
            postgresql_where="resolved = false",
        ),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    resolved: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    response: Optional[str] = None

    user_id: int = Field(foreign_key="users.id", nullable=False)
    user: Optional["Users"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[TrainerRequest.user_id]"}
    )

    admin_id: Optional[int] = Field(foreign_key="users.id", nullable=True, default=None)
    admin: Optional["Users"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[TrainerRequest.admin_id]"}
    )


class TrainerRequestCreate(TrainerRequestBase):
    pass


class TrainerRequestRead(TrainerRequestBase):
    id: int
    description: str
    user: "UsersRead"
    resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime]


class TrainerRequestUpdate(TrainerRequestBase):
    resolved: bool
    resolved_at: datetime
    response: str
    admin_id: int
