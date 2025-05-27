import requests

DEEZER_GENRE_MAP = {}


def load_deezer_genres():
    global DEEZER_GENRE_MAP
    url = "https://api.deezer.com/genre"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Build a dict: {genre_id: genre_name}
        DEEZER_GENRE_MAP = {genre["id"]: genre["name"] for genre in data["data"]}
    else:
        DEEZER_GENRE_MAP = {}


def get_genre_name_by_id(genre_id: int) -> str:
    return DEEZER_GENRE_MAP.get(genre_id, "Unknown")
