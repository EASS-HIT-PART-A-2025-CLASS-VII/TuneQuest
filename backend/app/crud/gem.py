from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.gem import Gem
from app.schemas.gem import GemCreate

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
