from fastapi import APIRouter, Query
from app.services.spotify import get_spotify_access_token
import requests

router = APIRouter(prefix="/spotify", tags=["spotify"])


@router.get("/track/{id}")
def get_track(id: str):
    token = get_spotify_access_token()

    response = requests.get(
        f"https://api.spotify.com/v1/tracks/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200:
        return {"error": "Failed to fetch track info"}

    return response.json()


@router.get("/search")
def search_tracks(query: str = Query(..., min_length=1)):
    token = get_spotify_access_token()

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": query, "type": "track", "limit": 30},
    )

    if response.status_code != 200:
        return {"error": "Spotify search failed"}

    data = response.json()
    return data.get("tracks", {}).get("items", [])
