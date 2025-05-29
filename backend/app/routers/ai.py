from fastapi import APIRouter, HTTPException
from app.services.ai import ask_gemini
from app.services.spotify_search import search_spotify_entities
from pydantic import BaseModel
import json
import re

router = APIRouter(prefix="/ai", tags=["ai"])


class AISpecificRequest(BaseModel):
    prompt: str
    type: str


class AIRequest(BaseModel):
    prompt: str


class AICompanionResponse(BaseModel):
    tracks: list[str]
    artists: list[str]
    albums: list[str]


@router.post("/recommend-home")
def ai_recommend_home(request: AIRequest):
    print(request)
    try:
        ai_response = ask_gemini(request.prompt)
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

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="AI response is not valid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend")
def ai_recommend(request: AISpecificRequest):
    try:
        ai_response = ask_gemini(request.prompt)

        names = [
            line.strip("- ").strip()
            for line in ai_response.strip().splitlines()
            if line.strip()
        ]

        enriched = search_spotify_entities(names, request.type)

        return {"results": enriched}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/companion")
async def ai_companion(request: AIRequest):
    print(request.prompt)
    system_prompt = (
        "Return *only* a valid JSON object with exactly 3 keys: 'tracks', 'artists', and 'albums'. "
        "Each key must map to an array of names (strings). "
        "No explanations or extra text — only valid JSON."
    )
    user_prompt = request.prompt
    full_prompt = f"User asked: '{user_prompt}'.\n{system_prompt}"
    print(full_prompt)
    ai_response_text = ask_gemini(full_prompt)
    print(ai_response_text)
    try:
        print("hey")
        cleaned_response = re.sub(
            r"```(?:json)?\n(.+?)\n```", r"\1", ai_response_text, flags=re.DOTALL
        )

        data = json.loads(cleaned_response)
        print(data)
        tracks = data.get("tracks", [])
        artists = data.get("artists", [])
        albums = data.get("albums", [])
        print(tracks)
        print(artists)
        print(albums)
        enriched_tracks = search_spotify_entities(tracks, "track") if tracks else []
        enriched_artists = search_spotify_entities(artists, "artist") if artists else []
        enriched_albums = search_spotify_entities(albums, "album") if albums else []

        print(enriched_tracks)
        print(enriched_artists)
        print(enriched_albums)
        return {
            "results": {
                "tracks": enriched_tracks,
                "artists": enriched_artists,
                "albums": enriched_albums,
            }
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="AI response is not valid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
