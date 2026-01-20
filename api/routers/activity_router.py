from typing import List, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, File, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import delete, select, update

from api.database import SessionDep
from api.models.activity_models import (
    Activity,
    ActivityCreate,
    ActivityFilters,
    ActivityMedia,
    ActivityMediaCreate,
    ActivityMediaRead,
    ActivityMediaUpdate,
    ActivityRead,
    ActivityReadLight,
    ActivityUpdate,
)
from api.models.reviews_models import (
    Review,
    ReviewCreate,
    ReviewCreateInput,
    ReviewRead,
)
from api.models.user_models import Users
from api.routers.review_router import create_review, get_reviews_by_content_id
from api.security.auth import JwtPayload, get_current_user, verify_jwt_token
from api.utils.files import save_file

router = APIRouter(prefix="/api/activities", tags=["Activities"])


@router.get("", response_model=list[ActivityRead] | list[ActivityReadLight])
def get_activities(
    session: SessionDep, light: bool = False, filters: ActivityFilters = Depends()
):
    if light:
        query = select(
            Activity.id,
            Activity.owner_id,
            Users.username.label("owner_username"),
            Activity.name,
            Activity.description,
            Activity.duration_minutes,
            Activity.image_url,
            Activity.difficulty,
            Activity.tags,
        ).join(Users, Activity.owner_id == Users.id)
    else:
        query = select(Activity)

    query = filters.apply(query)
    activities = session.exec(query).all()

    if not activities:
        return []

    # Get average ratings
    activity_ids = [a.id if not light else a.id for a in activities]
    avg_ratings = session.exec(
        select(
            Review.content_id,
            func.avg(Review.rating).label("avg_rating"),
        )
        .where(Review.content_type == "activity")
        .where(Review.content_id.in_(activity_ids))
        .group_by(Review.content_id)
    ).all()

    rating_map = {
        content_id: float(avg_rating) for content_id, avg_rating in avg_ratings
    }

    # Build result
    result = []
    for activity in activities:
        if light:
            activity_dict = activity._asdict()
            activity_dict["average_rating"] = rating_map.get(activity.id)
            result.append(activity_dict)
        else:
            activity_data = ActivityRead.model_validate(activity)
            activity_dict = activity_data.model_dump()
            activity_dict["average_rating"] = rating_map.get(activity.id)
            result.append(activity_dict)

    return result


@router.get("/{activity_id}", response_model=ActivityRead)
def get_activity(session: SessionDep, activity_id: int):
    stmt = (
        select(Activity, func.avg(Review.rating).label("avg_rating"))
        .join(
            Review,
            (Review.content_id == Activity.id) & (Review.content_type == "activity"),
            isouter=True,
        )
        .where(Activity.id == activity_id)
        .group_by(Activity.id)
    )

    row = session.exec(stmt).first()
    if not row:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity, avg_rating = row
    ar = ActivityRead.model_validate(activity, from_attributes=True)
    ar.average_rating = float(avg_rating) if avg_rating is not None else None
    return ar


@router.post("", response_model=ActivityRead)
async def create_activity(
    image: UploadFile,
    session: SessionDep,
    activity_in: str = Form(...),
    current_user: JwtPayload = Depends(get_current_user),
):

    activity_in_obj = ActivityCreate.model_validate_json(activity_in)

    activity_data = activity_in_obj.model_dump()
    activity_data["owner_id"] = current_user.id

    filename = await save_file(image)

    print("FILE:", filename)

    activity_data["image_url"] = filename
    activity = Activity.model_validate(activity_data)

    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity


@router.put("/{activity_id}", response_model=ActivityRead)
async def update_activity(
    session: SessionDep,
    activity_id: int,
    activity_update: str = Form(...),
    current_user: JwtPayload = Depends(get_current_user),
    image: UploadFile | None = None,
):

    update_data_obj = ActivityUpdate.model_validate_json(activity_update)
    update_data = update_data_obj.model_dump(exclude_unset=True)
    if image:
        filename = await save_file(image)
        update_data["image_url"] = filename
        # TODO: delete old image file

    statement = (
        update(Activity)
        .where((Activity.id == activity_id) & (Activity.owner_id == current_user.id))
        .values(**update_data)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = session.get(Activity, activity_id)
    return activity


@router.delete("/{activity_id}")
def delete_activity(
    session: SessionDep,
    activity_id: int,
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = delete(Activity).where(
        (Activity.id == activity_id) & (Activity.owner_id == current_user.id)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Activity not found")

    return {"ok": True}


@router.post("/media", response_model=ActivityMediaRead)
def create_media(media_in: ActivityMediaCreate, session: SessionDep):
    media = ActivityMedia.model_validate(media_in)
    session.add(media)
    session.commit()
    session.refresh(media)
    return media


@router.put("/media/{media_id}", response_model=ActivityMediaRead)
def update_media(session: SessionDep, media_id: int, media_update: ActivityMediaUpdate):
    update_data = media_update.model_dump(exclude_unset=True)
    statement = (
        update(ActivityMedia).where(ActivityMedia.id == media_id).values(**update_data)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Media not found")

    media = session.get(ActivityMedia, media_id)
    return media


@router.delete("/media/{media_id}")
def delete_media(session: SessionDep, media_id: int):
    statement = delete(ActivityMedia).where(ActivityMedia.id == media_id)
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Media not found")

    return {"ok": True}


@router.post("/{activity_id}/reviews", response_model=ReviewRead)
def post_review(
    review_in: ReviewCreateInput,
    activity_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    review = ReviewCreate(
        content_type="activity",
        content_id=activity_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )

    return create_review(review, session, current_user)


@router.get("/{activity_id}/reviews", response_model=List[ReviewRead])
def get_reviews(
    activity_id: int,
    session: SessionDep,
    user_id: Optional[int] = None,
):
    return get_reviews_by_content_id(session, activity_id, "activity", user_id)
