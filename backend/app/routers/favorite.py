from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.favorite import FavoriteRead
from app.crud.favorite import get_all_favorites
from app.core.db import get_db

router = APIRouter(prefix="/favorites", tags=["favorites"])
favorite_not_found = "Favorite track not found"


@router.get("/", response_model=list[FavoriteRead])
async def read_all_favorites(
    sort_by: str = None,
    ascending: bool = True,
    db: AsyncSession = Depends(get_db),
):
    result = await get_all_favorites(db, sort_by, ascending)
    if not result:
        raise HTTPException(status_code=404, detail="Favorite tracks not found")
    return result
