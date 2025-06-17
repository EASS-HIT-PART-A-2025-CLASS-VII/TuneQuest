import requests

# Global genre map
DEEZER_GENRE_MAP = {}

def load_deezer_genres():
    """Load Deezer genres into global map."""
    global DEEZER_GENRE_MAP
    response = requests.get("https://api.deezer.com/genre")
    if response.status_code == 200:
        data = response.json()
        DEEZER_GENRE_MAP = {genre["id"]: genre["name"] for genre in data["data"]}
    else:
        DEEZER_GENRE_MAP = {}

def get_genre_name_by_id(genre_id: int) -> str:
    """Get genre name by ID."""
    return DEEZER_GENRE_MAP.get(genre_id, "Unknown")
