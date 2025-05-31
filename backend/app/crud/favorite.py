from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.favorite import Favorite
from sqlalchemy import asc, desc
from typing import Optional


async def create_favorite(
    user_id: int,
    spotify_id: str,
    db: AsyncSession,
    type: Optional[str] = None,
):
    existing = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.spotify_id == spotify_id,
        )
    )
    if existing.scalar_one_or_none():
        return False

    new_favorite = Favorite(
        user_id=user_id,
        spotify_id=spotify_id,
        type=type,
    )
    db.add(new_favorite)
    await db.commit()
    await db.refresh(new_favorite)
    return True


async def get_all_favorites(
    db: AsyncSession, sort_by: str = None, ascending: bool = True
):
    query = select(Favorite)
    query = apply_sorting(query, Favorite, sort_by, ascending)
    result = await db.execute(query)
    return result.scalars().all()


async def get_all_user_favorites(
    user_id: int,
    db: AsyncSession,
    sort_by: str = None,
    ascending: bool = True,
    type: str = None,
):
    query = select(Favorite).where(Favorite.user_id == user_id)
    if type:
        query = query.where(Favorite.type == type)
    query = apply_sorting(query, Favorite, sort_by, ascending)
    result = await db.execute(query)
    return result.scalars().all()


async def get_favorite(
    user_id: int, spotify_id: str, db: AsyncSession, type: str = None
):
    query = select(Favorite).where(
        Favorite.user_id == user_id,
        Favorite.spotify_id == spotify_id,
    )
    if type:
        query = query.where(Favorite.type == type)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def erase_favorite(
    user_id: int, spotify_id: str, db: AsyncSession, type: str = None
):
    query = select(Favorite).where(
        Favorite.user_id == user_id,
        Favorite.spotify_id == spotify_id,
    )
    if type:
        query = query.where(Favorite.type == type)
    result = await db.execute(query)
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
