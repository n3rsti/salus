from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.database import create_db_and_tables
from api.routers import activity_router, program_router, tag_router, review_router,auth_router,user_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return "Bok!"

app.include_router(activity_router.router)
app.include_router(program_router.router)
app.include_router(tag_router.router)
app.include_router(review_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #change it, when * it is not secure !!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)