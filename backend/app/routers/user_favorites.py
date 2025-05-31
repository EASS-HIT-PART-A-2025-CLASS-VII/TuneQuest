from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.favorite import FavoriteCreate, FavoriteRead
from app.crud.favorite import (
    create_favorite,
    get_favorite,
    erase_favorite,
    get_all_user_favorites,
)
from app.core.db import get_db

router = APIRouter(prefix="/users/{user_id}/favorites", tags=["favorites"])
favorite_not_found = "Favorite not found"


@router.post("/", response_model=FavoriteRead)
async def add_favorite(
    favorite: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
):
    new_favorite = await create_favorite(favorite, db)
    if not new_favorite:
        raise HTTPException(
            status_code=400, detail="Favorite already favorited by the user"
        )
    return new_favorite


@router.get("/", response_model=list[FavoriteRead])
async def read_all_user_favorites(
    user_id: int,
    sort_by: Optional[str] = None,
    ascending: bool = True,
    type: Optional[str] = Query(
        None, description="Filter by favorite type: track, album, artist"
    ),
    db: AsyncSession = Depends(get_db),
):
    if type and type not in {"track", "album", "artist"}:
        raise HTTPException(status_code=400, detail="Invalid favorite type")

    result = await get_all_user_favorites(user_id, db, sort_by, ascending, type)
    if not result:
        raise HTTPException(status_code=404, detail="Favorites not found")
    return result


@router.get("/{spotify_id}", response_model=FavoriteRead)
async def read_favorite(
    user_id: int,
    spotify_id: str,
    type: Optional[str] = Query(
        None, description="Favorite type: track, album, artist"
    ),
    db: AsyncSession = Depends(get_db),
):
    if type and type not in {"track", "album", "artist"}:
        raise HTTPException(status_code=400, detail="Invalid favorite type")

    result = await get_favorite(user_id, spotify_id, db, type)
    if not result:
        raise HTTPException(status_code=404, detail=favorite_not_found)
    return result


@router.delete("/{spotify_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(
    user_id: int,
    spotify_id: str,
    type: Optional[str] = Query(
        None, description="Favorite type: track, album, artist"
    ),
    db: AsyncSession = Depends(get_db),
):
    result = await erase_favorite(user_id, spotify_id, db, type)
    if not result:
        raise HTTPException(status_code=404, detail=favorite_not_found)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
