from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.favorite import Favorite, FavoriteType
from sqlalchemy import asc, desc
from typing import List, Dict, Any, Callable, Optional
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


async def _fetch_spotify_data_in_batches_threaded(
    spotify_ids: List[str], fetch_func_sync: Callable[[List[str]], Any], batch_size: int
) -> List[Dict[str, Any]]:
    """
    Helper to fetch Spotify data in concurrent batches, running synchronous
    fetch functions in separate threads.
    """
    all_results = []
    if not spotify_ids:
        return all_results

    tasks = []
    for i in range(0, len(spotify_ids), batch_size):
        batch_ids = spotify_ids[i : i + batch_size]
        # Use asyncio.to_thread to run the synchronous function in a separate thread
        tasks.append(asyncio.to_thread(fetch_func_sync, batch_ids))

    # asyncio.gather will wait for all threads to complete
    batch_results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in batch_results:
        if isinstance(result, HTTPException):
            print(
                f"Warning: Error fetching batch for {fetch_func_sync.__name__}: {result.detail}"
            )
        elif isinstance(
            result, Exception
        ):  # Catch any other exceptions from the thread
            print(
                f"Warning: Unexpected error fetching batch for {fetch_func_sync.__name__}: {result}"
            )
        else:
            all_results.extend(result)
    return all_results


async def get_spotify_metadata_for_user_favorites(user_id: int, db: AsyncSession):
    favorites = await get_all_user_favorites(user_id, db)

    grouped = {"tracks": [], "artists": [], "albums": []}
    for fav in favorites:
        plural_type_key = fav.type.value + "s"
        if fav.type and plural_type_key in grouped:
            grouped[plural_type_key].append(fav.spotify_id)

    # Prepare the tasks for asyncio.gather using the new top-level helper
    # Pass the synchronous get_by_ids functions and their appropriate batch sizes
    tracks_task = _fetch_spotify_data_in_batches_threaded(
        grouped["tracks"], get_tracks_by_ids, 20
    )
    artists_task = _fetch_spotify_data_in_batches_threaded(
        grouped["artists"], get_artists_by_ids, 20
    )
    albums_task = _fetch_spotify_data_in_batches_threaded(
        grouped["albums"], get_albums_by_ids, 20
    )

    # Execute all tasks concurrently
    tracks, artists, albums = await asyncio.gather(
        tracks_task, artists_task, albums_task
    )

    metadata = {
        "tracks": tracks,
        "artists": artists,
        "albums": albums,
    }
    print(metadata)
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
