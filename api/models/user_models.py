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
    username: str = Field(
        sa_column=Column("username", String, unique=True, nullable=False)
    )
    email: Optional[str] = Field(
        default=None,
        sa_column=Column("email", String, unique=True, nullable=True),
        description="Primary email address used for contact or OAuth login",
    )
    role_id: int = Field(
        foreign_key="role.id", description="Identifier of the role assigned to the user"
    )


class Users(UsersBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: Optional[str] = Field(
        default=None,
        sa_column=Column("password", String, nullable=True),
        description="Argonv2 hashed user password when using credentials login",
    )
    oauth_provider: Optional[str] = Field(
        default=None,
        sa_column=Column("oauth_provider", String, nullable=True),
        description="OAuth provider identifier (e.g. google)",
    )
    oauth_sub: Optional[str] = Field(
        default=None,
        sa_column=Column("oauth_sub", String, unique=True, nullable=True),
        description="Subject identifier returned by the OAuth provider",
    )
    role: Optional[Role] = Relationship(back_populates="users")
    # TODO: uncomment when fixed
    # reviews: list["Review"] = Relationship(back_populates="user")


class UsersCreate(UsersBase):
    password: str


class UsersRead(UsersBase):
    id: int


class UsersUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
