from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from api.database import SessionDep
from api.models.program_models import (
    Program,
    ProgramRead,
    ProgramDay,
    ProgramCreate,
    ProgramUpdate,
)
from api.models.program_day_activities_link import ProgramDayActivityLink

# This file contains API endpoints related to Programs

router = APIRouter(prefix="/api/programs", tags=["Programs"])


@router.get("", response_model=list[ProgramRead])
def get_programs(session: SessionDep):
    programs = session.exec(select(Program)).all()

    if programs:
        return programs
    else:
        return []


@router.post("", response_model=ProgramRead)
def create_program(program_in: ProgramCreate, session: SessionDep):
    program_data = program_in.model_dump(exclude={"days"})
    program = Program.model_validate(program_data)
    session.add(program)
    session.flush()

    if program_in.days:
        days: List[ProgramDay] = []
        for day_in in program_in.days:
            day = ProgramDay(
                description=day_in.description,
                day_number=day_in.day_number,
                program_id=program.id,
            )
            session.add(day)
            days.append(day)

        session.flush()

        for day, day_in in zip(days, program_in.days):
            for activity_id in day_in.activities_ids:
                link = ProgramDayActivityLink(
                    program_day_id=day.id, activity_id=activity_id
                )
                session.add(link)

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


@router.get("/{program_id}", response_model=ProgramRead)
def get_program(session: SessionDep, program_id: int):
    program = session.get(Program, program_id)

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    return program


@router.delete("/{program_id}")
def delete_program(session: SessionDep, program_id: int):
    program = session.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    session.delete(program)
    session.commit()
    return {"ok": True}
