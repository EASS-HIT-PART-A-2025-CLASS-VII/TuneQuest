from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.db import get_db
from archive.crud.top_tracks import get_top_tracks

router = APIRouter(prefix="/top-tracks", tags=["top-tracks"])


@router.get("/")
async def read_top_tracks(
    period: str = Query("daily", enum=["daily", "weekly", "monthly", "yearly"]),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    top_tracks = await get_top_tracks(db, period, limit)
    return [
        {"track_id": track_id, "favorites_count": count}
        for track_id, count in top_tracks
    ]
