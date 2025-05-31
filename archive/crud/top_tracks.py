from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.favorite import Favorite
from datetime import datetime, timedelta, timezone


async def get_top_tracks(db: AsyncSession, period: str = "daily", limit: int = 10):
    now = datetime.now(timezone.utc)

    if period == "daily":
        from_time = now - timedelta(days=1)
    elif period == "weekly":
        from_time = now - timedelta(weeks=1)
    elif period == "monthly":
        from_time = now - timedelta(days=30)
    elif period == "yearly":
        from_time = now - timedelta(days=365)
    else:
        from_time = None

    query = select(
        Favorite.track_id, func.count(Favorite.track_id).label("favorites_count")
    )

    if from_time:
        query = query.where(Favorite.created_at >= from_time)

    query = query.group_by(Favorite.track_id)
    query = query.order_by(func.count(Favorite.track_id).desc())
    query = query.limit(limit)

    result = await db.execute(query)
    return result.all()  # returns list of (track_id, favorites_count) tuples
