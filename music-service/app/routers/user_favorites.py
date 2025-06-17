from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.favorite import FavoriteRead
from app.crud.favorite import (
    create_favorite,
    get_favorite,
    erase_favorite,
    get_all_user_favorites,
    get_spotify_metadata_for_user_favorites,
)
from app.core.db import get_db
from app.core.auth import get_current_user
from app.schemas.user import User

# User favorites endpoints
router = APIRouter(prefix="/favorites", tags=["favorites"])
favorite_not_found = "Favorite not found"
favorite_type_description = "Favorite type: track, album, artist"


@router.post("/", response_model=dict)
async def add_favorite(
    spotify_id: str,
    type: Optional[str] = Query(None, description=favorite_type_description),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a favorite item."""
    result = await create_favorite(current_user.id, spotify_id, db, type)
    return {"result": result is not None}


@router.get("/", response_model=list[FavoriteRead])
async def read_all_user_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all user favorites."""
    result = await get_all_user_favorites(current_user.id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Favorites not found")
    return result


@router.get("/spotify")
async def get_all_spotify_metadata_for_user_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get Spotify metadata for all favorites."""
    try:
        metadata = await get_spotify_metadata_for_user_favorites(current_user.id, db)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{spotify_id}", response_model=dict)
async def read_favorite(
    spotify_id: str,
    type: Optional[str] = Query(None, description=favorite_type_description),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if item is favorited."""
    if type and type not in {"track", "album", "artist"}:
        raise HTTPException(status_code=400, detail="Invalid favorite type")

    result = await get_favorite(current_user.id, spotify_id, db, type)
    return {"result": result is not None}


@router.delete("/{spotify_id}", status_code=200)
async def delete_favorite(
    spotify_id: str,
    type: Optional[str] = Query(None, description=favorite_type_description),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a favorite item."""
    result = await erase_favorite(current_user.id, spotify_id, db, type)
    return {"result": result is not None}
