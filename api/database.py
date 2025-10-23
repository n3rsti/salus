from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

postgresql_database_url = "postgresql://postgres:admin@localhost:5432/salus"
engine = create_engine(postgresql_database_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]