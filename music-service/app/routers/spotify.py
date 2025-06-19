from fastapi import APIRouter, Query, HTTPException
import requests
from typing import List
from app.services.spotify import (
    get_tracks_by_ids,
    get_artists_by_ids,
    get_albums_by_ids,
    get_spotify_access_token,
)
from app.services.spotify_search import search_spotify_entities

# Spotify API endpoints
router = APIRouter(prefix="/spotify", tags=["spotify"])


@router.get("/track/{id}")
def get_track(id: str):
    """Get Spotify track info."""
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
    """Get Spotify artist info."""
    token = get_spotify_access_token()
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch artist info")
    return response.json()


@router.get("/artist/{id}/top-tracks")
def get_artist_top_tracks(id: str, market: str = "US"):
    """Get artist's top tracks."""
    token = get_spotify_access_token()
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{id}/top-tracks?market={market}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch top tracks")
    return response.json()


@router.get("/artist/{id}/albums")
def get_artist_albums(id: str, include_groups: str = "album,single"):
    """Get artist's albums."""
    token = get_spotify_access_token()
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{id}/albums",
        headers={"Authorization": f"Bearer {token}"},
        params={"include_groups": include_groups},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch albums")
    return response.json()


@router.get("/album/{id}")
def get_album(id: str):
    """Get Spotify album info."""
    token = get_spotify_access_token()
    response = requests.get(
        f"https://api.spotify.com/v1/albums/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch album info")
    return response.json()


@router.get("/tracks")
def get_tracks(ids: List[str] = Query(..., description="List of Spotify tracks IDs")):
    """Get multiple tracks by IDs."""
    try:
        tracks = get_tracks_by_ids(ids)
        return {"tracks": tracks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/artists")
def get_artists(ids: List[str] = Query(..., description="List of Spotify artists IDs")):
    """Get multiple artists by IDs."""
    try:
        artists = get_artists_by_ids(ids)
        return {"artists": artists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/albums")
def get_albums(ids: List[str] = Query(..., description="List of Spotify album IDs")):
    try:
        albums = get_albums_by_ids(ids)
        return {"albums": albums}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Spotify search failed")

    return response.json()


@router.get("/entities")
def get_spotify_entities(
    names: List[str] = Query(..., description="List of names to search"),
    type_: str = Query(..., description="Entity type: track, artist, or album"),
):
    print("8")
    return search_spotify_entities(names, type_)
