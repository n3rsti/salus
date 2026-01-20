from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import func
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
from api.models.reviews_models import (
    Review,
    ReviewCreate,
    ReviewCreateInput,
    ReviewRead,
)
from api.security.auth import JwtPayload, get_current_user
from api.utils.files import save_file

from api.routers.review_router import create_review, get_reviews_by_content_id

router = APIRouter(prefix="/api/programs", tags=["Programs"])


@router.get("", response_model=list[ProgramRead])
def get_programs(session: SessionDep, filters: ProgramFilters = Depends()):
    avg_subq = (
        select(
            Review.content_id.label("program_id"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .where(Review.content_type == "program")
        .group_by(Review.content_id)
        .subquery()
    )

    query = select(Program, avg_subq.c.avg_rating).join(
        avg_subq, avg_subq.c.program_id == Program.id, isouter=True
    )

    query = filters.apply(query)

    rows = session.exec(query).all()
    if not rows:
        return []

    result: list[ProgramRead] = []
    for program, avg_rating in rows:
        pr = ProgramRead.model_validate(program, from_attributes=True)
        pr.average_rating = float(avg_rating) if avg_rating is not None else None
        result.append(pr)

    return result


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
async def update_program(
    program_id: int,
    session: SessionDep,
    program_update: str = Form(...),
    image: UploadFile | None = None,
    current_user: JwtPayload = Depends(get_current_user),
):
    program_update_obj = ProgramUpdate.model_validate_json(program_update)

    update_data = program_update_obj.model_dump(exclude_unset=True, exclude={"days"})

    if image is not None:
        image_url = await save_file(image)
        update_data["image_url"] = image_url

    if update_data:
        statement = (
            update(Program)
            .where((Program.id == program_id) & (Program.owner_id == current_user.id))
            .values(**update_data)
        )
        result = session.exec(statement)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Program not found")

    if program_update_obj.days is not None:
        program = session.exec(
            select(Program).where(
                (Program.id == program_id) & (Program.owner_id == current_user.id)
            )
        ).first()
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

        session.exec(delete(ProgramDay).where(ProgramDay.program_id == program_id))
        session.flush()
        link_days(session, program_id, program_update_obj.days)

    session.commit()

    program = session.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


@router.get("/{program_id}", response_model=ProgramRead)
def get_program(program_id: int, session: SessionDep):
    program = session.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    avg_rating = session.exec(
        select(func.avg(Review.rating)).where(
            Review.content_type == "program", Review.content_id == program_id
        )
    ).first()

    program_data = ProgramRead.model_validate(program)

    result = program_data.model_dump()
    result["average_rating"] = round(float(avg_rating), 2) if avg_rating else None

    return result


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


@router.post("/{program_id}/reviews", response_model=ReviewRead)
def post_review(
    review_in: ReviewCreateInput,
    program_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    review = ReviewCreate(
        content_type="program",
        content_id=program_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )

    return create_review(review, session, current_user)


@router.get("/{program_id}/reviews", response_model=List[ReviewRead])
def get_reviews(
    program_id: int,
    session: SessionDep,
    user_id: Optional[int] = None,
):
    return get_reviews_by_content_id(session, program_id, "program", user_id)
