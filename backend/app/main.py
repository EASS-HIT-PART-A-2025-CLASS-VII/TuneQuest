from fastapi import FastAPI
from app.models.base import Base
from app.core.db import SessionLocal, engine
from app.routers import track, user
from contextlib import asynccontextmanager


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(track.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hidden tracks Finder API is up and running!"}
