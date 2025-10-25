from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from database import SessionDep
from models.program_models import Activity, ActivityMedia, ActivityRead, ActivityMediaRead

# This file contains API endpoints related to Activities

router = APIRouter(prefix="/api/activities", tags=["Activities"])

@router.post("/", response_model=Activity)
def create_activity(activity: Activity, session: SessionDep):
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@router.get("/", response_model=list[ActivityRead])
def get_activities(session: SessionDep):
    activities = session.exec(select(Activity)).all()

    if activities:
        return activities
    else:
        return []

@router.delete("/{activity_id}")
def delete_activity(session: SessionDep, activity_id: int):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    session.delete(activity)
    session.commit()
    return {"ok": True}

@router.put("/{activity_id}", response_model=Activity)
def update_activity(session: SessionDep, activity_id: int, activity_updated: Activity):
    activity = session.get(Activity, activity_id)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity.name = activity_updated.name
    activity.duration_minutes = activity_updated.duration_minutes
    activity.description = activity_updated.description
    activity.difficulty = activity_updated.difficulty

    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@router.post("/media", response_model=ActivityMedia)
def create_media(media: ActivityMedia, session: SessionDep):
    activity = session.get(Activity, media.activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

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