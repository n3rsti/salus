from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from database import SessionDep
from models.program_models import Activity, ActivityMedia, ActivityRead, ActivityMediaRead, ActivityCreate, ActivityUpdate, ActivityMediaCreate, ActivityMediaUpdate

# This file contains API endpoints related to Activities

router = APIRouter(prefix="/api/activities", tags=["Activities"])

@router.get("/", response_model=list[ActivityRead])
def get_activities(session: SessionDep):
    activities = session.exec(select(Activity)).all()

    if activities:
        return activities
    else:
        return []

@router.post("/", response_model=ActivityRead)
def create_activity(activity_in: ActivityCreate, session: SessionDep):
    activity = Activity.model_validate(activity_in)

    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@router.put("/{activity_id}", response_model=ActivityRead)
def update_activity(session: SessionDep, activity_id: int, activity_update: ActivityUpdate):
    activity = session.get(Activity, activity_id)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    update_data = activity_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(activity, key, value)

    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@router.delete("/{activity_id}")
def delete_activity(session: SessionDep, activity_id: int):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    session.delete(activity)
    session.commit()
    return {"ok": True}

@router.post("/media", response_model=ActivityMediaRead)
def create_media(media_in: ActivityMediaCreate, session: SessionDep):
    activity = session.get(Activity, media_in.activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail=f"Activity with id={media_in.activity_id} not found")

    media = ActivityMedia.model_validate(media_in)
    session.add(media)
    session.commit()
    session.refresh(media)
    return media

@router.put("/media/{media_id}", response_model=ActivityMediaRead)
def update_media(session: SessionDep, media_id: int, media_update: ActivityMediaUpdate):
    media = session.get(ActivityMedia, media_id)

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    if media_update.activity_id != None:
        activity = session.get(Activity, media_update.activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail=f"Activity with id={media_update.activity_id} not found")

    update_data = media_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(media, key, value)

    session.add(media)
    session.commit()
    session.refresh(media)
    return media

@router.delete("/media/{media_id}")
def delete_media(media: ActivityMedia, session: SessionDep, media_id: int):
    media = session.get(ActivityMedia, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    session.delete(media)
    session.commit()
    return {"ok": True}