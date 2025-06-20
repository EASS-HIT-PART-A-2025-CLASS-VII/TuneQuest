import requests
import os
from fastapi import HTTPException
from typing import List

# Spotify API endpoints
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_TRACKS_URL = "https://api.spotify.com/v1/tracks"
SPOTIFY_ARTISTS_URL = "https://api.spotify.com/v1/artists"
SPOTIFY_ALBUMS_URL = "https://api.spotify.com/v1/albums"


def get_spotify_access_token():
    """Get Spotify API access token."""
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="Missing Spotify credentials")

    response = requests.post(
        SPOTIFY_TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500, detail="Failed to authenticate with Spotify"
        )

    return response.json()["access_token"]


def get_tracks_by_ids(ids: List[str]):
    """Get Spotify tracks by IDs."""
    token = get_spotify_access_token()
    if len(ids) > 10:
        raise ValueError("Can fetch a maximum of 10 tracks per request")

    headers = {"Authorization": f"Bearer {token}"}
    params = {"ids": ",".join(ids)}
    response = requests.get(SPOTIFY_TRACKS_URL, headers=headers, params=params)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(
            f"Spotify API error: {response.status_code} - {response.text}"
        ) from e

    data = response.json()
    return data.get("tracks", [])


def get_artists_by_ids(ids: List[str]):
    """Get Spotify artists by IDs."""
    token = get_spotify_access_token()
    if len(ids) > 10:
        raise ValueError("Can fetch a maximum of 10 artists per request")

    headers = {"Authorization": f"Bearer {token}"}
    params = {"ids": ",".join(ids)}
    response = requests.get(SPOTIFY_ARTISTS_URL, headers=headers, params=params)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(
            f"Spotify API error: {response.status_code} - {response.text}"
        ) from e

    data = response.json()
    return data.get("artists", [])


def get_albums_by_ids(ids: List[str]):
    """Get Spotify albums by IDs."""
    token = get_spotify_access_token()
    if len(ids) > 10:
        raise ValueError("Can fetch a maximum of 10 albums per request")

    headers = {"Authorization": f"Bearer {token}"}
    params = {"ids": ",".join(ids)}
    response = requests.get(SPOTIFY_ALBUMS_URL, headers=headers, params=params)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(
            f"Spotify API error: {response.status_code} - {response.text}"
        ) from e

    data = response.json()
    return data.get("albums", [])
