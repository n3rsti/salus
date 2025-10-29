from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from database import SessionDep
from models.program_models import Tag, TagRead, Program
from models.programs_tags_link import ProgramTagLink

# This file contains API endpoints related to Tags

router = APIRouter(prefix="/api/tags", tags=["Tags"])

@router.get("/", response_model=list[TagRead])
def get_tags(session: SessionDep):
    tags = session.exec(select(Tag)).all()

    if tags:
        return tags
    else:
        return []

@router.post("/", response_model=Tag)
def create_tag(tag: Tag, session: SessionDep):
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag

@router.delete("/{tag_id}")
def delete_tag(session: SessionDep, tag_id: int):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag)
    session.commit()
    return {"ok": True}

@router.put("/{tag_id}", response_model=Tag)
def update_tag(session: SessionDep, tag_id: int, tag_updated: Tag):
    tag = session.get(Tag, tag_id)

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.name = tag_updated.name
    tag.icon = tag_updated.icon

    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag

@router.post("/{tag_id}/programs/{program_id}")
def link_tag_to_program(tag_id: int, program_id: int, session: SessionDep):
    tag = session.get(Tag, tag_id)
    program = session.get(Program, program_id)

    if not tag or not program:
        raise HTTPException(status_code=404, detail="Tag or Program not found")

    link = ProgramTagLink(program_id=program_id, tag_id=tag_id)
    session.add(link)
    session.commit()
    return {"ok": True, "message": f"Tag {tag_id} linked to Program {program_id}"}