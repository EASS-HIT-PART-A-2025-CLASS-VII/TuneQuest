from fastapi import APIRouter, Depends, HTTPException, status
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
favorite_not_found = "Favorite track not found"


@router.post("/", response_model=FavoriteRead)
async def add_favorite(
    favorite: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
):
    new_favorite = await create_favorite(favorite, db)
    if not new_favorite:
        raise HTTPException(
            status_code=400, detail="Track already favorited by the user"
        )
    return new_favorite


@router.get("/", response_model=list[FavoriteRead])
async def read_all_user_favorites(
    user_id: int,
    sort_by: str = None,
    ascending: bool = True,
    db: AsyncSession = Depends(get_db),
):
    result = await get_all_user_favorites(user_id, db, sort_by, ascending)
    if not result:
        raise HTTPException(status_code=404, detail="Favorite tracks not found")
    return result


@router.get("/{favorite_id}", response_model=FavoriteRead)
async def read_favorite(
    user_id: int, favorite_id: int, db: AsyncSession = Depends(get_db)
):
    result = await get_favorite(user_id, favorite_id, db)
    if not result:
        raise HTTPException(status_code=404, detail=favorite_not_found)
    return result


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(
    user_id: int, favorite_id: int, db: AsyncSession = Depends(get_db)
):
    result = await erase_favorite(user_id, favorite_id, db)
    if not result:
        raise HTTPException(status_code=404, detail=favorite_not_found)
