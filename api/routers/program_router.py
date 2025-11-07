from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from database import SessionDep
from models.program_models import Program, ProgramRead, ProgramDay, ProgramDayCreate,ProgramDayUpdate, Activity, ProgramCreate, ProgramUpdate
from models.program_day_activities_link import ProgramDayActivityLink

# This file contains API endpoints related to Programs

router = APIRouter(prefix="/api/programs", tags=["Programs"])

@router.get("/", response_model=list[ProgramRead])
def get_programs(session: SessionDep):
    programs = session.exec(select(Program)).all()

    if programs:
        return programs
    else:
        return []

@router.post("/", response_model=ProgramRead)
def create_program(program_in: ProgramCreate, session: SessionDep):
    program = Program.model_validate(program_in)
    session.add(program)
    session.commit()
    session.refresh(program)
    return program

@router.put("/{program_id}", response_model=ProgramRead)
def update_program(session: SessionDep, program_id: int, program_update: ProgramUpdate):
    program = session.get(Program, program_id)

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    update_data = program_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(program, key, value)

    session.add(program)
    session.commit()
    session.refresh(program)
    return program

@router.delete("/{program_id}")
def delete_program(session: SessionDep, program_id: int):
    program = session.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    session.delete(program)
    session.commit()
    return {"ok": True}

@router.post("/days", response_model=ProgramDay)
def create_program_day(day_in: ProgramDayCreate, session: SessionDep):
    program = session.get(Program, day_in.program_id)
    if not program:
        raise HTTPException(status_code=404, detail=f"Program with id={day_in.program_id} not found")

    day = ProgramDay.model_validate(day_in)
    session.add(day)
    session.commit()
    session.refresh(day)
    return day

@router.put("/days/{program_day_id}", response_model=ProgramDay)
def update_program_day(session: SessionDep, program_day_id: int, program_day_update: ProgramDayUpdate):
    program_day = session.get(ProgramDay, program_day_id)

    if not program_day:
        raise HTTPException(status_code=404, detail="Program day not found")

    if program_day_update.program_id != None:
        program = session.get(Program, program_day_update.program_id)
        if not program:
            raise HTTPException(status_code=404, detail=f"Program with id={program_day_update.program_id} not found")

    update_data = program_day_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(program_day, key, value)

    session.add(program_day)
    session.commit()
    session.refresh(program_day)
    return program_day

@router.delete("/days/{program_day_id}")
def delete_program_day(session: SessionDep, program_day_id: int):
    program_day = session.get(ProgramDay, program_day_id)
    if not program_day:
        raise HTTPException(status_code=404, detail="Program day not found")
    session.delete(program_day)
    session.commit()
    return {"ok": True}

@router.post("/days/{program_day_id}/activities/{activity_id}")
def link_activity_to_program_day(program_day_id: int, activity_id: int, session: SessionDep):
    program_day = session.get(ProgramDay, program_day_id)
    activity = session.get(Activity, activity_id)

    if not program_day or not activity:
        raise HTTPException(status_code=404, detail="ProgramDay or Activity not found")

    link = ProgramDayActivityLink(program_day_id=program_day_id, activity_id=activity_id)
    session.add(link)
    session.commit()
    return {"ok": True, "message": f"Activity {activity_id} linked to ProgramDay {program_day_id}"}