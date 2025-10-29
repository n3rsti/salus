from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from database import SessionDep
from models.reviews_models import Review, ReviewRead, ReviewCreate, ReviewUpdate
from models.program_models import Program, Activity

# This file contains API endpoints related to Reviews

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

@router.get("/", response_model=list[ReviewRead])
def get_reviews(session: SessionDep):
    reviews = session.exec(select(Review)).all()

    if reviews:
        return reviews
    else:
        return []

@router.post("/", response_model=ReviewRead)
def create_review(review_in: ReviewCreate, session: SessionDep):
    if review_in.content_type == "program":
        content = session.exec(select(Program).where(Program.id == review_in.content_id)).first()
    elif review_in.content_type == "activity":
        content = session.exec(select(Activity).where(Activity.id == review_in.content_id)).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid content_type")

    if not content:
        raise HTTPException(
            status_code=404,
            detail=f"{review_in.content_type.capitalize()} with id={review_in.content_id} not found"
        )

    review = Review.model_validate(review_in)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review

@router.delete("/{review_id}")
def delete_review(session: SessionDep, review_id: int):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return {"ok": True}

@router.put("/{review_id}", response_model=ReviewRead)
def update_review(review_id: int, review_update: ReviewUpdate, session: SessionDep):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)

    session.add(review)
    session.commit()
    session.refresh(review)

    return review