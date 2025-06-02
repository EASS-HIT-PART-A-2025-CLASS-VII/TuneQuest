from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.favorite import Favorite, FavoriteType
from sqlalchemy import asc, desc
from typing import Optional, List
from app.services.spotify import (
    get_tracks_by_ids,
    get_artists_by_ids,
    get_albums_by_ids,
)
from fastapi import HTTPException
import asyncio


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

    favorite_type_enum = None
    if type:
        try:
            favorite_type_enum = FavoriteType[type]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid favorite type: '{type}'. Must be 'track', 'album', or 'artist'.",
            )
    else:
        raise HTTPException(status_code=400, detail="Favorite type is required.")

    new_favorite = Favorite(
        user_id=user_id,
        spotify_id=spotify_id,
        type=favorite_type_enum,
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
):
    query = select(Favorite).where(Favorite.user_id == user_id)
    query = apply_sorting(query, Favorite)
    result = await db.execute(query)
    return result.scalars().all()


async def get_spotify_metadata_for_user_favorites(user_id: int, db: AsyncSession):
    favorites = await get_all_user_favorites(user_id, db)

    grouped = {"tracks": [], "artists": [], "albums": []}
    for fav in favorites:
        plural_type_key = fav.type.value + "s"
        # Use fav.type.value to get the string representation for the dictionary key
        if (
            fav.type and plural_type_key in grouped
        ):  # Defensive check for unexpected types
            print("hey")
            grouped[plural_type_key].append(fav.spotify_id)

    metadata = {
        "tracks": [],
        "artists": [],
        "albums": [],
    }  # Initialize with empty lists for safety

    # Helper function for batching Spotify API calls
    async def fetch_spotify_data_in_batches(spotify_ids: List[str], fetch_func):
        all_results = []
        if not spotify_ids:
            return all_results
        # Spotify API limit is 20 ids per request (or adjust if your function allows more)
        for i in range(0, len(spotify_ids), 20):
            batch_ids = spotify_ids[i : i + 20]
            try:
                batch_data = await fetch_func(batch_ids)
                all_results.extend(batch_data)
            except HTTPException as e:
                print(
                    f"Warning: Error fetching batch for {fetch_func.__name__}: {e.detail}"
                )
                # You might choose to re-raise, or just skip this batch
                # For now, we'll let the main try-except in router handle a 500 if unhandled here
        return all_results

    tracks_task = fetch_spotify_data_in_batches(grouped["tracks"], get_tracks_by_ids)
    artists_task = fetch_spotify_data_in_batches(grouped["artists"], get_artists_by_ids)
    albums_task = fetch_spotify_data_in_batches(grouped["albums"], get_albums_by_ids)

    tracks, artists, albums = await asyncio.gather(
        tracks_task, artists_task, albums_task
    )

    metadata["tracks"] = tracks
    metadata["artists"] = artists
    metadata["albums"] = albums

    return metadata


async def get_favorite(
    user_id: int, spotify_id: str, db: AsyncSession, type: str = None
):
    query = select(Favorite).where(
        Favorite.user_id == user_id,
        Favorite.spotify_id == spotify_id,
    )
    if type:
        try:
            query = query.where(Favorite.type == FavoriteType[type])
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid favorite type: '{type}'. Must be 'track', 'album', or 'artist'.",
            )
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
        try:
            query = query.where(Favorite.type == FavoriteType[type])
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid favorite type: '{type}'. Must be 'track', 'album', or 'artist'.",
            )
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
