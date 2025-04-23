from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.gem import Gem, Base
from app.core.db import SessionLocal, engine
from app.routers import gem


app = FastAPI()
app.include_router(gem.router)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    # Creates tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/gems")
async def get_gems(db: AsyncSession = Depends(get_db)):
    # Async query to fetch all gems
    result = await db.execute(select(Gem))
    gems = result.scalars().all()  # Extract gem objects from the result
    return gems

@app.get("/")
async def root():
    return {"message": "Hidden Gems Finder API is up and running!"}
