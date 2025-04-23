from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.gem import Gem, GemCreate, GemUpdate, GemReplace
from app.crud.gem import (
    create_gem,
    get_all_gems,
    get_gem,
    delete_gem,
    update_gem,
    update_gem_full,
)
from app.core.db import SessionLocal

router = APIRouter(prefix="/gems", tags=["Gems"])
gem_not_found = "Gem not found"
VALID_SORT_FIELDS = {"name", "rating", "category", "id"}


# Dependency to get a DB session
async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/", response_model=Gem)
async def create_gem_endpoint(gem: GemCreate, db: AsyncSession = Depends(get_db)):
    return await create_gem(db, gem)


@router.get("/", response_model=list[Gem])
async def read_all_gems(
    category: str | None = None,
    location: str | None = None,
    sort: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    # Validate sort field
    if sort and sort not in VALID_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Choose from: {', '.join(VALID_SORT_FIELDS)}",
        )
    return await get_all_gems(db, category, location, sort)


@router.get("/{gem_id}", response_model=Gem)
async def read_gem(gem_id: int, db: AsyncSession = Depends(get_db)):
    gem = await get_gem(db, gem_id)
    if not gem:
        raise HTTPException(status_code=404, detail=gem_not_found)
    return gem


@router.delete("/{gem_id}", response_model=bool)
async def delete_gem_endpoint(gem_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_gem(db, gem_id)
    if not success:
        raise HTTPException(status_code=404, detail=gem_not_found)
    return True


@router.patch("/{gem_id}", response_model=Gem)
async def update_gem_endpoint(
    gem_id: int, gem_update: GemUpdate, db: AsyncSession = Depends(get_db)
):
    updated_gem = await update_gem(db, gem_id, gem_update)
    if not updated_gem:
        raise HTTPException(status_code=404, detail=gem_not_found)
    return updated_gem


@router.put("/{gem_id}", response_model=Gem)
async def update_gem_full_endpoint(
    gem_id: int, gem_replace: GemReplace, db: AsyncSession = Depends(get_db)
):
    replaced_gem = await update_gem_full(db, gem_id, gem_replace)
    if not replaced_gem:
        raise HTTPException(status_code=404, detail="Gem not found")
    return replaced_gem
