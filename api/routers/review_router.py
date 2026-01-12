from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import delete, select, update

from api.database import SessionDep
from api.models.reviews_models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from api.security.auth import JwtPayload, get_current_user

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@router.get("", response_model=List[ReviewRead])
def get_reviews(session: SessionDep):
    reviews = session.exec(select(Review)).all()
    return reviews if reviews else []


@router.post("", response_model=ReviewRead)
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
    statement = delete(Review).where(
        (Review.id == review_id) & (Review.user_id == current_user.id)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Review not found")

    return {"ok": True}
