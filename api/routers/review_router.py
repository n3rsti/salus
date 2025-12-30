from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from typing import List

from api.database import SessionDep
from api.models.reviews_models import Review, ReviewRead, ReviewCreate, ReviewUpdate
from api.models.program_models import Program, Activity
from api.models.user_models import Users
from api.security.auth import JwtPayload, get_current_user

# This file contains API endpoints related to Reviews with user validation

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
    if review_in.content_type == "program":
        content = session.get(Program, review_in.content_id)
    elif review_in.content_type == "activity":
        content = session.get(Activity, review_in.content_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid content_type")

    if not content:
        raise HTTPException(
            status_code=404,
            detail=f"{review_in.content_type.capitalize()} with id={review_in.content_id} not found",
        )

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
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not enough permissions to edit this review"
        )

    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)

    session.add(review)
    session.commit()
    session.refresh(review)
    return review


@router.delete("/{review_id}")
def delete_review(
    session: SessionDep,
    review_id: int,
    current_user: Users = Depends(get_current_active_user),
):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    is_owner = review.user_id == current_user.id
    is_privileged_user = current_user.role in ["admin"]

    if not (is_owner or is_privileged_user):
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to delete this review. Only owner or admin can do this.",
        )

    session.delete(review)
    session.commit()
    return {"ok": True}
