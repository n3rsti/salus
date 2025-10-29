from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import activity_router, program_router, tag_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(activity_router.router)
app.include_router(program_router.router)
app.include_router(tag_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #change it, when * it is not secure !!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)