from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

from database import create_db_and_tables, SessionDep
from db_models import Activity


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/activities", response_model=Activity)
def create_activity(activity: Activity, session: SessionDep):
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@app.get("/activities", response_model=list[Activity])
def get_activities(session: SessionDep):
    activities = session.exec(select(Activity)).all()
    if activities:
        return activities
    else:
        raise HTTPException(status_code=404, detail="No activity found")
