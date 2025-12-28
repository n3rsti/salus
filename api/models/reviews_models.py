from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import field_validator


class ReviewBase(SQLModel):
    # user_id: int | None = Field(default=None, foreign_key="users.id", ondelete="CASCADE")
    content_type: str = Field(description="Either 'program' or 'activity'")
    content_id: int
    rating: int
    comment: Optional[str] = None

    @field_validator("content_type")
    def validate_content_type(cls, v):
        if v not in {"program", "activity"}:
            raise ValueError("content_type must be 'program' or 'activity'")
        return v

    @field_validator("rating")
    def validate_rating(cls, v):
        if v is None:
            return v
        if not (1 <= v <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return v


class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(SQLModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

    @field_validator("rating")
    def validate_rating(cls, v):
        if v is None:
            return v
        if not (1 <= v <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return v


class ReviewRead(ReviewBase):
    id: int
    created_at: datetime
