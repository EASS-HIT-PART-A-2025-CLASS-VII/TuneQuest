import requests
import os
from fastapi import HTTPException

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"


def get_spotify_access_token():
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
