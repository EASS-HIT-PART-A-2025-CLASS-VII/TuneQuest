from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.favorite import FavoriteRead
from app.crud.favorite import (
    create_favorite,
    get_favorite,
    erase_favorite,
    get_all_user_favorites,
)
from app.core.db import get_db
from app.core.auth import get_current_user
from app.models.user import User


router = APIRouter(prefix="/favorites", tags=["favorites"])
favorite_not_found = "Favorite not found"
type = "Favorite type: track, album, artist"


@router.post("/", response_model=dict)
async def add_favorite(
    spotify_id: str,
    type: Optional[str] = Query(None, description=type),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await create_favorite(current_user.id, spotify_id, db, type)
    return {"result": result is not None}


@router.get("/", response_model=list[FavoriteRead])
async def read_all_user_favorites(
    sort_by: Optional[str] = None,
    ascending: bool = True,
    type: Optional[str] = Query(None, description=type),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if type and type not in {"track", "album", "artist"}:
        raise HTTPException(status_code=400, detail="Invalid favorite type")

    result = await get_all_user_favorites(current_user.id, db, sort_by, ascending, type)
    if not result:
        raise HTTPException(status_code=404, detail="Favorites not found")
    return result


@router.get("/{spotify_id}", response_model=dict)
async def read_favorite(
    spotify_id: str,
    type: Optional[str] = Query(None, description=type),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if type and type not in {"track", "album", "artist"}:
        raise HTTPException(status_code=400, detail="Invalid favorite type")

    result = await get_favorite(current_user.id, spotify_id, db, type)
    return {"result": result is not None}


@router.delete("/{spotify_id}", status_code=dict)
async def delete_favorite(
    spotify_id: str,
    type: Optional[str] = Query(None, description=type),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await erase_favorite(current_user.id, spotify_id, db, type)
    return {"result": result is not None}
