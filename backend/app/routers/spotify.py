from fastapi import APIRouter, Query
from app.services.spotify import get_spotify_access_token
import requests

router = APIRouter(prefix="/spotify", tags=["spotify"])


@router.get("/search")
def search_tracks(query: str = Query(..., min_length=1)):
    token = get_spotify_access_token()

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": query, "type": "track", "limit": 10},
    )

    if response.status_code != 200:
        return {"error": "Spotify search failed"}

    data = response.json()
    return data.get("tracks", {}).get("items", [])
