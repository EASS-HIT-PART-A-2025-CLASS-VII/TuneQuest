from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.gem import Gem
from app.schemas.gem import GemCreate, GemUpdate

# Create a new gem in the DB
async def create_gem(db: AsyncSession, gem: GemCreate):
    new_gem = Gem(**gem.dict())
    db.add(new_gem)
    await db.commit()
    await db.refresh(new_gem)
    return new_gem

# Get all gems from the DB
async def get_all_gems(db: AsyncSession):
    result = await db.execute(select(Gem))
    return result.scalars().all()

# Get a gem by ID
async def get_gem(db: AsyncSession, gem_id: int):
    result = await db.execute(select(Gem).where(Gem.id == gem_id))
    return result.scalars().first()

async def delete_gem(db: AsyncSession, gem_id: int) -> bool:
    # Fetch the gem to delete
    result = await db.execute(select(Gem).filter(Gem.id == gem_id))
    gem = result.scalar_one_or_none()

    if gem:
        # Delete the gem
        await db.delete(gem)
        await db.commit()
        return True
    return False

async def update_gem(db: AsyncSession, gem_id: int, gem_update: GemUpdate):
    # Fetch the existing gem from the database
    result = await db.execute(select(Gem).where(Gem.id == gem_id))
    gem = result.scalar_one_or_none()

    if not gem:
        return None  # Gem not found

    # Update only the fields provided in the patch
    if gem_update.name is not None:
        gem.name = gem_update.name
    if gem_update.location is not None:
        gem.location = gem_update.location
    if gem_update.description is not None:
        gem.description = gem_update.description
    if gem_update.rating is not None:
        gem.rating = gem_update.rating
    if gem_update.category is not None:
        gem.category = gem_update.category

    # Commit the changes to the database
    await db.commit()
    await db.refresh(gem)  # Refresh to get updated data
    return gem

async def update_gem_full(db: AsyncSession, gem_id: int, gem_data: GemCreate):
    result = await db.execute(
        select(Gem).where(Gem.id == gem_id)
    )
    gem = result.scalar_one_or_none()

    if not gem:
        return None

    gem.name = gem_data.name
    gem.location = gem_data.location
    gem.description = gem_data.description
    gem.rating = gem_data.rating
    gem.category = gem_data.category

    await db.commit()
    await db.refresh(gem)
    return gem
