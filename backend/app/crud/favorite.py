from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate
from sqlalchemy import asc, desc


async def create_favorite(favorite: FavoriteCreate, db: AsyncSession):
    existing = await db.execute(
        select(Favorite).where(
            Favorite.user_id == favorite.user_id,
            Favorite.spotify_id == favorite.spotify_id,
        )
    )
    if existing.scalar_one_or_none():
        return None
    new_favorite = Favorite(**favorite.model_dump())
    db.add(new_favorite)
    await db.commit()
    await db.refresh(new_favorite)
    return new_favorite


async def get_all_favorites(
    db: AsyncSession, sort_by: str = None, ascending: bool = True
):
    query = select(Favorite)
    query = apply_sorting(query, Favorite, sort_by, ascending)
    result = await db.execute(query)
    return result.scalars().all()


async def get_all_user_favorites(
    user_id: int, db: AsyncSession, sort_by: str = None, ascending: bool = True
):
    query = select(Favorite).where(Favorite.user_id == user_id)
    query = apply_sorting(query, Favorite, sort_by, ascending)
    result = await db.execute(query)
    return result.scalars().all()


async def get_favorite(user_id: int, spotify_id: str, db: AsyncSession):
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.spotify_id == spotify_id,
        )
    )
    return result.scalar_one_or_none()


async def erase_favorite(user_id: int, spotify_id: str, db: AsyncSession):
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.spotify_id == spotify_id,
        )
    )
    favorite = result.scalar_one_or_none()
    if not favorite:
        return False

    await db.delete(favorite)
    await db.commit()
    return True


def apply_sorting(query, model, sort_by: str = None, ascending: bool = True):
    if sort_by and hasattr(model, sort_by):
        column = getattr(model, sort_by)
        return query.order_by(asc(column) if ascending else desc(column))
    return query
