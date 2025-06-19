import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List

# Initialize Spotify client
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))


def search_spotify_entities(names: List[str], type_: str):
    """Search Spotify for entities by name and type."""
    results = []

    for name in names:
        try:
            query = f"{name}"
            search = sp.search(q=query, type=type_, limit=1)
            items = search.get(f"{type_}s", {}).get("items", [])
            if not items:
                continue
            item = items[0]
            result = {
                "name": item.get("name"),
                "id": item.get("id"),
                "type": type_,
                "image": item.get("images", [{}])[0].get("url")
                if type_ != "track"
                else item["album"]["images"][0]["url"],
                "url": item.get("external_urls", {}).get("spotify"),
            }
            results.append(result)

        except Exception:
            continue

    return results
