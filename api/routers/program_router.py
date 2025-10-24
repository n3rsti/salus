from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from database import SessionDep
from models.program_models import Program, ProgramRead, ProgramDay, ProgramDayRead

router = APIRouter(prefix="/api/programs", tags=["Programs"])

@router.get("/", response_model=list[ProgramRead])
def get_programs(session: SessionDep):
    programs = session.exec(select(Program)).all()

    if programs:
        return programs
    else:
        return []

@router.post("/", response_model=Program)
def create_program(program: Program, session: SessionDep):
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

@router.put("/{program_id}", response_model=Program)
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


@router.post("/days", response_model=ProgramDay)
def create_program_day(day: ProgramDay, session: SessionDep):
    program = session.get(Program, day.program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    session.add(day)
    session.commit()
    session.refresh(day)
    return day

@router.delete("/days/{program_day_id}")
def delete_program_day(session: SessionDep, program_day_id: int):
    program_day = session.get(ProgramDay, program_day_id)
    if not program_day:
        raise HTTPException(status_code=404, detail="Program day not found")
    session.delete(program_day)
    session.commit()
    return {"ok": True}

@router.put("/days/{program_day_id}", response_model=ProgramDay)
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
