from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.database import create_db_and_tables
from api.routers import (
    activity_router,
    program_router,
    review_router,
    auth_router,
    trainer_router,
    user_router,
    emotion_router,
    daily_log_router,
    user_preference_router,
    activity_plan_router,
    user_activity_router,
    recommendation_router,
)
from api.utils.files import UPLOAD_DIR

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return "Bok!"


app.mount("/media", StaticFiles(directory=UPLOAD_DIR), name="media")


app.include_router(activity_router.router)
app.include_router(program_router.router)
app.include_router(review_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(emotion_router.router)
app.include_router(daily_log_router.router)
app.include_router(user_preference_router.router)
app.include_router(activity_plan_router.router)
app.include_router(user_activity_router.router)
app.include_router(recommendation_router.router)
app.include_router(trainer_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change it, when * it is not secure !!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
