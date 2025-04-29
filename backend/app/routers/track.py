from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.track import (
    TrackRead,
    TrackCreate,
    TrackUpdate,
    TrackReplace,
)
from app.crud.track import (
    create_track,
    get_all_tracks,
    get_track,
    delete_track,
    update_track,
    update_track_full,
)
from app.core.db import get_db

router = APIRouter(prefix="/tracks", tags=["tracks"])
track_not_found = "Track not found"
VALID_SORT_FIELDS = {"id", "title", "artist", "album", "genre", "rating"}


@router.post("/", response_model=TrackRead)
async def create_track_endpoint(track: TrackCreate, db: AsyncSession = Depends(get_db)):
    new_track = await create_track(track, db)
    if not new_track:
        raise HTTPException(status_code=400, detail="Track already exists")
    return new_track


@router.get("/all", response_model=list[TrackRead])
async def read_all_tracks(
    genre: str | None = None,
    artist: str | None = None,
    sort: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    # Handle sort validation
    validated_sort = []
    if sort:
        fields = sort.split(",")
        for field in fields:
            clean_field = field.lstrip("-")  # remove leading "-" for validation
            if clean_field not in VALID_SORT_FIELDS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid sort field: {clean_field}. Choose from: {', '.join(VALID_SORT_FIELDS)}",
                )
        validated_sort = fields

    return await get_all_tracks(db, genre, artist, validated_sort)


@router.get("/{track_id}", response_model=TrackRead)
async def read_track(track_id: int, db: AsyncSession = Depends(get_db)):
    track = await get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=404, detail=track_not_found)
    return track


@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_track_endpoint(track_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_track(db, track_id)
    if not success:
        raise HTTPException(status_code=404, detail=track_not_found)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{track_id}", response_model=TrackRead)
async def update_track_endpoint(
    track_id: int, track_update: TrackUpdate, db: AsyncSession = Depends(get_db)
):
    updated_track = await update_track(db, track_id, track_update)
    if not updated_track:
        raise HTTPException(status_code=404, detail=track_not_found)
    return updated_track


@router.put("/{track_id}", response_model=TrackRead)
async def update_track_full_endpoint(
    track_id: int, track_replace: TrackReplace, db: AsyncSession = Depends(get_db)
):
    replaced_track = await update_track_full(db, track_id, track_replace)
    if not replaced_track:
        raise HTTPException(status_code=404, detail="Track not found")
    return replaced_track
