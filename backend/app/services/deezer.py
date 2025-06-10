import requests

# Deezer API endpoints
def fetch_deezer_genres(album: str, artist: str):
    """Get Deezer genre for album and artist."""
    query = f"{album} {artist}"
    response = requests.get("https://api.deezer.com/search/album", params={"q": query})
    response.raise_for_status()
    data = response.json()

    if not data["data"]:
        return None

    genre_id = data["data"][0].get("genre_id")
    if not genre_id:
        return None

    genre_response = requests.get(f"https://api.deezer.com/genre/{genre_id}")
    genre_response.raise_for_status()
    genre_data = genre_response.json()

    return genre_data.get("name")

def fetch_deezer_preview_url(track_name, artist_name):
    """Get Deezer preview URL for track."""
    query = f"{track_name} {artist_name}"
    response = requests.get("https://api.deezer.com/search/track", params={"q": query})
    response.raise_for_status()
    data = response.json()

    if not data["data"]:
        return None

    return data["data"][0].get("preview")
