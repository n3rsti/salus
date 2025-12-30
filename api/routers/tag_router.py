from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import delete, select, update

from api.database import SessionDep
from api.models.programs_tags_link import ProgramTagLink
from api.models.tag_models import Program, Tag, TagCreate, TagRead, TagUpdate
from api.security.auth import JwtPayload, get_current_user

router = APIRouter(prefix="/api/tags", tags=["Tags"])


@router.get("", response_model=list[TagRead])
def get_tags(session: SessionDep):
    tags = session.exec(select(Tag)).all()

    if tags:
        return tags
    else:
        return []


@router.post("", response_model=TagRead)
def create_tag(tag_in: TagCreate, session: SessionDep):
    tag = Tag.model_validate(tag_in)

    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.put("/{tag_id}", response_model=TagRead)
def update_tag(session: SessionDep, tag_id: int, tag_update: TagUpdate):
    update_data = tag_update.model_dump(exclude_unset=True)
    statement = update(Tag).where(Tag.id == tag_id).values(**update_data)
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag = session.get(Tag, tag_id)
    return tag


@router.delete("/{tag_id}")
def delete_tag(session: SessionDep, tag_id: int):
    statement = delete(Tag).where(Tag.id == tag_id)
    result = session.exec(statement)
    session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tag not found")

    return {"ok": True}


@router.post("/{tag_id}/programs/{program_id}")
def link_tag_to_program(
    tag_id: int,
    program_id: int,
    session: SessionDep,
    current_user: JwtPayload = Depends(get_current_user),
):
    link = ProgramTagLink(program_id=program_id, tag_id=tag_id)
    session.add(link)
    session.commit()
    return {"ok": True, "message": f"Tag {tag_id} linked to Program {program_id}"}
