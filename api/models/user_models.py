from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

# avoid circular import using TYPE_CHECKING:
if TYPE_CHECKING:
    from models.reviews_models import Review

class RoleBase(SQLModel):
    name: str = Field(sa_column=Column("name", String, unique=True, nullable=False))

class Role(RoleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users: List["Users"] = Relationship(back_populates="role")

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: int

class UsersBase(SQLModel):
    username: str = Field(sa_column=Column("username", String, unique=True, nullable=False))
    role_id: int = Field(foreign_key="role.id", description="Identifier of the role assigned to the user")

class Users(UsersBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field(
        sa_column=Column("password", String, nullable=False),
        description="hashed user password",
    )
    role: Optional[Role] = Relationship(back_populates="users")
    reviews: list["Review"] = Relationship(back_populates="user")

class UsersCreate(UsersBase):
    password: str

class UsersRead(UsersBase):
    id: int

class UsersUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None