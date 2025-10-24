from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from dotenv import dotenv_values

config = dotenv_values(".env")

user = config.get("POSTGRES_USER", "postgres")
password = config.get("POSTGRES_PASSWORD", "admin")
db = config.get("POSTGRES_DB", "salus")
host = config.get("POSTGRES_HOST", "localhost")

postgresql_database_url = f"postgresql://{user}:{password}@{host}:5432/{db}"
engine = create_engine(postgresql_database_url, echo=True)


def create_db_and_tables():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

