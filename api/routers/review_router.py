from calendar import c
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import state
from sqlmodel import delete, select, update

from api.database import SessionDep
from api.models.reviews_models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from api.security.auth import JwtPayload, get_current_user, is_admin

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@router.get("", response_model=List[ReviewRead])
def get_reviews(session: SessionDep):
    reviews = session.exec(select(Review)).all()
    return reviews if reviews else []


def create_review(
    review_in: ReviewCreate,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    review_data = review_in.model_dump()
    review_data["user_id"] = current_user.id

    review = Review.model_validate(review_data)

    session.add(review)
    session.commit()
    session.refresh(review)

    return review


def get_reviews_by_content_id(
    session: SessionDep,
    content_id: int,
    content_type: str,
    user_id: Optional[int] = None,
    limit: int = 10,
):
    statement = select(Review).where(
        Review.content_id == content_id, Review.content_type == content_type
    )

    if user_id:
        statement = statement.order_by(
            (Review.user_id == user_id).desc(), Review.created_at.desc()
        )
    else:
        statement = statement.order_by(Review.created_at.desc())

    statement = statement.limit(limit)

    return session.exec(statement).all()


def delete_review_by_content_id(
    session: SessionDep,
    content_id: int,
    content_type: str,
):
    statement = delete(Review).where(
        Review.content_id == content_id, Review.content_type == content_type
    )

    result = session.exec(statement)
    session.commit()


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    update_data = review_update.model_dump(exclude_unset=True)
    statement = (
        update(Review)
        .where((Review.id == review_id) & (Review.user_id == current_user.id))
        .values(**update_data)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Review not found")

    review = session.get(Review, review_id)
    return review


@router.delete("/{review_id}")
def delete_review(
    session: SessionDep,
    review_id: int,
    current_user: JwtPayload = Depends(get_current_user),
):
    if is_admin(current_user):
        statement = delete(Review).where((Review.id == review_id))
    else:
        statement = delete(Review).where(
            (Review.id == review_id) & (Review.user_id == current_user.id)
        )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Review not found")

    return {"ok": True}
