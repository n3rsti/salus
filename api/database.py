from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine, select
from dotenv import dotenv_values
from api.models.user_models import Role

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

    #vvvv to be removed later
    with Session(engine) as session:
        result = session.exec(select(Role).where(Role.name == "user")).first()
        if not result:
            default_role = Role(id=1, name="user")
            session.add(default_role)
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
