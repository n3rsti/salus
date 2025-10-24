from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.orm import selectinload

from database import create_db_and_tables, SessionDep
from db_models import Activity, ActivityMedia, ActivityRead, ActivityMediaRead, Program, ProgramRead, ProgramDay, ProgramDayRead


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

    if activities:
        return activities
    else:
        return []

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

@app.delete("/api/activities/media/{media_id}")
def delete_media(media: ActivityMedia, session: SessionDep, media_id: int):
    media = session.get(ActivityMedia, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    session.delete(media)
    session.commit()
    return {"ok": True}



@app.get("/api/programs", response_model=list[ProgramRead])
def get_programs(session: SessionDep):
    programs = session.exec(select(Program)).all()

    if programs:
        return programs
    else:
        return []

@app.post("/api/programs", response_model=Program)
def create_program(program: Program, session: SessionDep):
    session.add(program)
    session.commit()
    session.refresh(program)
    return program

@app.delete("/api/programs/{program_id}")
def delete_program(session: SessionDep, program_id: int):
    program = session.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    session.delete(program)
    session.commit()
    return {"ok": True}

@app.put("/api/programs/{program_id}", response_model=Program)
def update_program(session: SessionDep, program_id: int, program_updated: Program):
    program = session.get(Program, program_id)

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    program.name = program_updated.name
    program.duration_days = program_updated.duration_days
    program.description = program_updated.description
    program.language = program_updated.language

    session.add(program)
    session.commit()
    session.refresh(program)
    return program


@app.post("/api/programs/days", response_model=ProgramDay)
def create_program_day(day: ProgramDay, session: SessionDep):
    program = session.get(Program, day.program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    session.add(day)
    session.commit()
    session.refresh(day)
    return day

@app.delete("/api/programs/days/{program_day_id}")
def delete_program_day(session: SessionDep, program_day_id: int):
    program_day = session.get(ProgramDay, program_day_id)
    if not program_day:
        raise HTTPException(status_code=404, detail="Program day not found")
    session.delete(program_day)
    session.commit()
    return {"ok": True}

@app.put("/api/programs/days/{program_day_id}", response_model=ProgramDay)
def update_program_day(session: SessionDep, program_day_id: int, program_day_updated: ProgramDay):
    program_day = session.get(ProgramDay, program_day_id)

    if not program_day:
        raise HTTPException(status_code=404, detail="Program day not found")

    program_day.description = program_day_updated.description
    program_day.day_number = program_day_updated.day_number

    session.add(program_day)
    session.commit()
    session.refresh(program_day)
    return program_day
