from fastapi import APIRouter, HTTPException
from app.services.deezer import fetch_deezer_genres

router = APIRouter()


@router.get("/deezer/genres")
def get_deezer_genres(album: str, artist: str):
    try:
        genre_name = fetch_deezer_genres(album, artist)
        return {"genre": genre_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
