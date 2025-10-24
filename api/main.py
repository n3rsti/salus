from fastapi import FastAPI
from database import create_db_and_tables
from routers import activity_router, program_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(activity_router.router)
app.include_router(program_router.router)