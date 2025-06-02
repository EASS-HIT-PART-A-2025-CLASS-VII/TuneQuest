from app.services.ai import ask_gemini
import re
import json
from app.services.spotify_search import search_spotify_entities
from app.schemas.ai import AISpecificRequest


def get_recommendations_home(request: str):
    ai_response = ask_gemini(request)
    cleaned_response = re.sub(
        r"```(?:json)?\n(.+?)\n```", r"\1", ai_response, flags=re.DOTALL
    )
    data = json.loads(cleaned_response)

    tracks = data.get("tracks", [])
    artists = data.get("artists", [])
    albums = data.get("albums", [])

    enriched_tracks = search_spotify_entities(tracks, "track") if tracks else []
    enriched_artists = search_spotify_entities(artists, "artist") if artists else []
    enriched_albums = search_spotify_entities(albums, "album") if albums else []

    return {
        "results": {
            "tracks": enriched_tracks,
            "artists": enriched_artists,
            "albums": enriched_albums,
        }
    }


def get_recommendations_button(request: AISpecificRequest):
    ai_response = ask_gemini(request.prompt)

    names = [
        line.strip("- ").strip()
        for line in ai_response.strip().splitlines()
        if line.strip()
    ]

    enriched = search_spotify_entities(names, request.type)

    return {"results": enriched}


def get_companion(request: str):
    system_prompt = (
        "Return *only* a valid JSON object with exactly 3 keys: 'tracks', 'artists', and 'albums'. "
        "Each key must map to an array of names (strings). "
        "No explanations or extra text — only valid JSON."
    )
    user_prompt = request
    full_prompt = f"User asked: '{user_prompt}'.\n{system_prompt}"
    ai_response_text = ask_gemini(full_prompt)

    cleaned_response = re.sub(
        r"```(?:json)?\n(.+?)\n```", r"\1", ai_response_text, flags=re.DOTALL
    )

    data = json.loads(cleaned_response)

    tracks = data.get("tracks", [])
    artists = data.get("artists", [])
    albums = data.get("albums", [])

    enriched_tracks = search_spotify_entities(tracks, "track") if tracks else []
    enriched_artists = search_spotify_entities(artists, "artist") if artists else []
    enriched_albums = search_spotify_entities(albums, "album") if albums else []

    return {
        "results": {
            "tracks": enriched_tracks,
            "artists": enriched_artists,
            "albums": enriched_albums,
        }
    }
