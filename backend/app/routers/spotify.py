from fastapi import APIRouter, Query, HTTPException
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
        raise HTTPException(status_code=502, detail="Failed to fetch track info")

    return response.json()


@router.get("/artist/{id}")
def get_artist(id: str):
    token = get_spotify_access_token()

    response = requests.get(
        f"https://api.spotify.com/v1/artists/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch artist info")

    return response.json()


@router.get("/album/{id}")
def get_albums(id: str):
    token = get_spotify_access_token()

    response = requests.get(
        f"https://api.spotify.com/v1/albums/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch album info")
    return response.json()


@router.get("/search")
def search(query: str = Query(..., min_length=1)):
    token = get_spotify_access_token()

    try:
        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers={"Authorization": f"Bearer {token}"},
            params={"q": query, "type": "track,artist,album", "limit": 30},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching from Spotify API: {e}")
        raise HTTPException(status_code=502, detail="Spotify search failed")

    return response.json()
