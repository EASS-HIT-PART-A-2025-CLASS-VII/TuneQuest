from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.gem import Gem, GemCreate
from app.crud.gem import create_gem, get_all_gems, get_gem
from app.core.db import SessionLocal

router = APIRouter(prefix="/gems", tags=["Gems"])

# Dependency to get a DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=Gem)
async def create_gem_endpoint(gem: GemCreate, db: AsyncSession = Depends(get_db)):
    return await create_gem(db, gem)

@router.get("/", response_model=list[Gem])
async def read_all_gems(db: AsyncSession = Depends(get_db)):
    return await get_all_gems(db)

@router.get("/{gem_id}", response_model=Gem)
async def read_gem(gem_id: int, db: AsyncSession = Depends(get_db)):
    gem = await get_gem(db, gem_id)
    if not gem:
        raise HTTPException(status_code=404, detail="Gem not found")
    return gem
