from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.track import Track
from app.schemas.track import TrackCreate, TrackUpdate, TrackReplace
from sqlalchemy import asc, desc


# Create a new track in the DB
async def create_track(db: AsyncSession, track: TrackCreate):
    new_track = Track(**track.model_dump())
    db.add(new_track)
    await db.commit()
    await db.refresh(new_track)
    return new_track


# Get all tracks from the DB (assumes validated input)
async def get_all_tracks(
    db: AsyncSession,
    genre: str | None = None,
    artist: str | None = None,
    sort: list[str] | None = None,
):
    query = select(Track)

    if genre:
        query = query.where(Track.genre == genre)
    if artist:
        query = query.where(Track.artist == artist)

    if sort:
        sort_expressions = []
        for field in sort:
            direction = asc
            if field.startswith("-"):
                direction = desc
                field = field[1:]

            sort_column = getattr(Track, field, None)
            if sort_column is not None:
                sort_expressions.append(direction(sort_column))

        if sort_expressions:
            query = query.order_by(*sort_expressions)

    else:
        query = query.order_by(Track.id.asc())  # fallback to default sort

    result = await db.execute(query)
    return result.scalars().all()


# Get a track by ID
async def get_track(db: AsyncSession, track_id: int):
    result = await db.execute(select(Track).where(Track.id == track_id))
    return result.scalars().first()


async def delete_track(db: AsyncSession, track_id: int) -> bool:
    # Fetch the track to delete
    result = await db.execute(select(Track).filter(Track.id == track_id))
    track = result.scalar_one_or_none()

    if track:
        # Delete the track
        await db.delete(track)
        await db.commit()
        return True
    return False


async def update_track(db: AsyncSession, track_id: int, track_update: TrackUpdate):
    # Fetch the existing track from the database
    result = await db.execute(select(Track).where(Track.id == track_id))
    track = result.scalar_one_or_none()

    if not track:
        return None  # track not found

    # Update only the fields provided in the patch
    if track_update.title is not None:
        track.title = track_update.title
    if track_update.artist is not None:
        track.artist = track_update.artist
    if track_update.album is not None:
        track.album = track_update.album
    if track_update.rating is not None:
        track.rating = track_update.rating
    if track_update.genre is not None:
        track.genre = track_update.genre

    # Commit the changes to the database
    await db.commit()
    await db.refresh(track)  # Refresh to get updated data
    return track


async def update_track_full(db: AsyncSession, track_id: int, track_data: TrackReplace):
    result = await db.execute(select(Track).where(Track.id == track_id))
    track = result.scalar_one_or_none()

    if not track:
        return None

    track.title = track_data.title
    track.artist = track_data.artist
    track.album = track_data.album
    track.rating = track_data.rating
    track.genre = track_data.genre

    await db.commit()
    await db.refresh(track)
    return track
