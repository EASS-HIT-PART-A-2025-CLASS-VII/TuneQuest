from fastapi import APIRouter, HTTPException, status
from app.services.deezer import fetch_deezer_genres, fetch_deezer_preview_url

router = APIRouter()


@router.get("/deezer/genres")
def get_deezer_genres(album: str, artist: str):
    try:
        genre_name = fetch_deezer_genres(album, artist)
        return {"genre": genre_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/deezer/tracks")
def get_deezer_preview_url(track: str, artist: str):
    try:
        preview_url = fetch_deezer_preview_url(track, artist)
        if not preview_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Preview not found"
            )
        return {"preview_url": preview_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
