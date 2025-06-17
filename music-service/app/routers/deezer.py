from fastapi import APIRouter, HTTPException, status
from app.services.deezer import fetch_deezer_genres, fetch_deezer_preview_url

# Deezer API endpoints
router = APIRouter(prefix="/deezer", tags=["deezer"])


@router.get("/genres")
def get_deezer_genres(album: str, artist: str):
    """Get Deezer genre info."""
    try:
        genre_name = fetch_deezer_genres(album, artist)
        return {"genre": genre_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tracks")
def get_deezer_preview_url(track: str, artist: str):
    """Get Deezer track preview URL."""
    try:
        preview_url = fetch_deezer_preview_url(track, artist)
        if not preview_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Preview not found"
            )
        return {"preview_url": preview_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
