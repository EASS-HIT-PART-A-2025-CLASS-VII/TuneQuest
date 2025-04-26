from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.track import Track as TrackModel, Base
from app.core.db import SessionLocal, engine
from app.routers import track
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


@app.get("/tracks")
async def get_tracks(db: AsyncSession = Depends(get_db)):
    # Async query to fetch all tracks
    result = await db.execute(select(TrackModel))
    tracks = result.scalars().all()
    return tracks


@app.get("/")
async def root():
    return {"message": "Hidden tracks Finder API is up and running!"}
