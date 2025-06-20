from fastapi import FastAPI
from app.models.base import Base
from app.core.db import init_db
from app.routers import (
    user,
    ai,
)
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database and get the engine
    db_engine = init_db()
    if not db_engine:
        raise RuntimeError("Failed to initialize database")

    # Startup: create tables
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(ai.router)


@app.get("/")
async def root():
    return {"message": "Hidden tracks Finder API is up and running!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
