from fastapi import APIRouter, Depends, Form, HTTPException, File, UploadFile
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
    ActivityUpdate,
)
from api.models.user_models import Users
from api.security.auth import JwtPayload, get_current_user, verify_jwt_token
from api.utils.files import save_file

router = APIRouter(prefix="/api/activities", tags=["Activities"])


@router.get("", response_model=list[ActivityRead])
def get_activities(session: SessionDep, filters: ActivityFilters = Depends()):
    query = select(Activity)
    query = filters.apply(query)
    activities = session.exec(query).all()

    if activities:
        return activities
    else:
        return []


@router.get("/{activity_id}", response_model=ActivityRead)
def get_activity(session: SessionDep, activity_id: int):
    activity = session.get(Activity, activity_id)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    return activity


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
