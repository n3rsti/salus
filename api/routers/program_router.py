from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, delete

from api.database import SessionDep
from api.models.program_models import (
    Program,
    ProgramDayInput,
    ProgramFilters,
    ProgramRead,
    ProgramDay,
    ProgramCreate,
    ProgramUpdate,
)
from api.models.program_day_activities_link import ProgramDayActivityLink
from api.security.auth import get_current_user
from api.models.user_models import Users

# This file contains API endpoints related to Programs

router = APIRouter(prefix="/api/programs", tags=["Programs"])


@router.get("", response_model=list[ProgramRead])
def get_programs(session: SessionDep, filters: ProgramFilters = Depends()):
    query = select(Program)
    query = filters.apply(query)
    programs = session.exec(query).all()

    if programs:
        return programs
    else:
        return []


def link_days(session: SessionDep, program_id: int, days_in: List[ProgramDayInput]):
    days = []
    for day_in in days_in:
        day = ProgramDay(
            description=day_in.description,
            day_number=day_in.day_number,
            program_id=program_id,
        )
        session.add(day)
        days.append(day)

    session.flush()

    for day, day_in in zip(days, days_in):
        for activity_id in day_in.activities_ids:
            link = ProgramDayActivityLink(
                program_day_id=day.id, activity_id=activity_id
            )
            session.add(link)


@router.post("", response_model=ProgramRead)
def create_program(
    program_in: ProgramCreate,
    session: SessionDep,
    current_user: int = Depends(get_current_user),
):
    program_data = program_in.model_dump(exclude={"days"})
    program_data["owner_id"] = current_user
    program = Program.model_validate(program_data)

    session.add(program)
    session.flush()

    if program_in.days and program.id:
        link_days(session, program.id, program_in.days)

    session.commit()
    session.refresh(program)
    return program


@router.put("/{program_id}", response_model=ProgramRead)
def update_program(
    session: SessionDep,
    program_id: int,
    program_update: ProgramUpdate,
    current_user: int = Depends(get_current_user),
):
    program = session.get(Program, program_id)

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    if program.owner_id != current_user:
        raise HTTPException(
            status_code=403, detail="Not enough permissions to edit this program"
        )

    update_data = program_update.model_dump(exclude_unset=True, exclude={"days"})
    for key, value in update_data.items():
        setattr(program, key, value)

    session.add(program)

    if program_update.days:
        session.exec(delete(ProgramDay).where(ProgramDay.program_id == program_id))
        session.flush()
        link_days(session, program_id, program_update.days)

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
def delete_program(
    session: SessionDep,
    program_id: int,
    current_user: int = Depends(get_current_user),
):
    program = session.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    if program.owner_id != current_user:
        raise HTTPException(
            status_code=403, detail="Not enough permissions to delete this program"
        )

    session.delete(program)
    session.commit()
    return {"ok": True}
