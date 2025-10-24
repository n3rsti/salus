from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.orm import selectinload

from database import create_db_and_tables, SessionDep
from db_models import Activity, ActivityMedia, ActivityRead, ActivityMediaRead


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/api/activities", response_model=Activity)
def create_activity(activity: Activity, session: SessionDep):
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@app.get("/api/activities", response_model=list[ActivityRead])
def get_activities(session: SessionDep):
    activities = session.exec(select(Activity)).all()

    # activities = session.exec(
    #     select(Activity).options(selectinload(Activity.media))
    # ).all()

    if activities:
        return activities
    else:
        raise HTTPException(status_code=404, detail="No activity found")

@app.delete("/api/activities/{activity_id}")
def delete_activity(session: SessionDep, activity_id: int):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    session.delete(activity)
    session.commit()
    return {"ok": True}

@app.put("/api/activities/{activity_id}", response_model=Activity)
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

@app.post("/api/activites/media", response_model=ActivityMedia)
def create_media(media: ActivityMedia, session: SessionDep):
    activity = session.get(Activity, media.activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    session.add(media)
    session.commit()
    session.refresh(media)
    return media
