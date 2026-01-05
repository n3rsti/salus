from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from sqlmodel import delete, select, update

from api.database import SessionDep
from api.models.program_day_activities_link import ProgramDayActivityLink
from api.models.program_models import (
    Program,
    ProgramCreate,
    ProgramDay,
    ProgramDayInput,
    ProgramFilters,
    ProgramRead,
    ProgramUpdate,
)
from api.security.auth import JwtPayload, get_current_user
from api.utils.files import save_file

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
async def create_program(
    image: UploadFile,
    session: SessionDep,
    program_in: str = Form(...),
    current_user: JwtPayload = Depends(get_current_user),
):
    program_create = ProgramCreate.model_validate_json(program_in)

    program_data = program_create.model_dump(exclude={"days"})
    program_data["owner_id"] = current_user.id

    image_url = await save_file(image)
    program_data["image_url"] = image_url

    program = Program.model_validate(program_data)
    session.add(program)
    session.flush()

    if program.id and program_create.days:
        link_days(session, program.id, program_create.days)

    session.commit()
    session.refresh(program)
    return program


@router.put("/{program_id}", response_model=ProgramRead)
def update_program(
    session: SessionDep,
    program_id: int,
    program_update: ProgramUpdate,
    current_user: JwtPayload = Depends(get_current_user),
):
    update_data = program_update.model_dump(exclude_unset=True, exclude={"days"})

    if update_data:
        statement = (
            update(Program)
            .where((Program.id == program_id) & (Program.owner_id == current_user.id))
            .values(**update_data)
        )
        result = session.exec(statement)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Program not found")

    if program_update.days:
        statement = select(Program).where(
            (Program.id == program_id) & (Program.owner_id == current_user.id)
        )
        program = session.exec(statement).first()

        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

        session.exec(delete(ProgramDay).where(ProgramDay.program_id == program_id))
        session.flush()
        link_days(session, program_id, program_update.days)

    session.commit()
    program = session.get(Program, program_id)
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
    current_user: JwtPayload = Depends(get_current_user),
):
    statement = delete(Program).where(
        (Program.id == program_id) & (Program.owner_id == current_user.id)
    )
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Program not found")

    return {"ok": True}
