from app.services.ai import ask_gemini
import re
import json
from app.schemas.ai import AISpecificRequest
from app.models.history import AiHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
# AI history operations


async def get_recommendations_home(request: str):
    """Get AI home recommendations."""
    ai_response = ask_gemini(request)
    cleaned_response = re.sub(
        r"```(?:json)?\n(.+?)\n```", r"\1", ai_response, flags=re.DOTALL
    )
    data = json.loads(cleaned_response)
    tracks = data.get("tracks", [])
    artists = data.get("artists", [])
    albums = data.get("albums", [])

    print("tracks:", tracks, type(tracks))
    print("artists:", artists, type(artists))
    print("albums:", albums, type(albums))

    enriched_tracks = await search_spotify_entities(tracks, "track") if tracks else []
    enriched_artists = (
        await search_spotify_entities(artists, "artist") if artists else []
    )
    enriched_albums = await search_spotify_entities(albums, "album") if albums else []

    return {
        "results": {
            "tracks": enriched_tracks,
            "artists": enriched_artists,
            "albums": enriched_albums,
        }
    }


async def get_recommendations_button(request: AISpecificRequest):
    """Get AI button recommendations."""
    ai_response = ask_gemini(request.prompt)
    names = [
        line.strip("- ").strip()
        for line in ai_response.strip().splitlines()
        if line.strip()
    ]
    enriched = await search_spotify_entities(names, request.type)
    return {"results": enriched}


async def get_companion(db: AsyncSession, prompt: str, user_id: int = None):
    """Get AI companion response."""
    system_prompt = (
        "Return *only* a valid JSON object with exactly 3 keys: 'tracks', 'artists', and 'albums'. "
        "Each key must map to an array of names (strings). "
        "No explanations or extra text — only valid JSON."
    )
    full_prompt = f"User asked: '{prompt}'.\n{system_prompt}"
    ai_response_text = ask_gemini(full_prompt)
    match = re.search(r"```(?:json)?\s*(.+?)\s*```", ai_response_text, flags=re.DOTALL)
    if match:
        extracted_content = match.group(1)
        cleaned_response = " ".join(extracted_content.split()).strip()
    else:
        cleaned_response = " ".join(ai_response_text.split()).strip()
    try:
        data = json.loads(cleaned_response)
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Failed to parse AI JSON", cleaned_response, 0)

    tracks = data.get("tracks", [])
    artists = data.get("artists", [])
    albums = data.get("albums", [])

    enriched_tracks = await search_spotify_entities(tracks, "track") if tracks else []
    enriched_artists = (
        await search_spotify_entities(artists, "artist") if artists else []
    )
    enriched_albums = await search_spotify_entities(albums, "album") if albums else []
    result = {
        "results": {
            "tracks": enriched_tracks,
            "artists": enriched_artists,
            "albums": enriched_albums,
        }
    }
    if user_id is not None:
        try:
            entry = AiHistory(
                user_id=user_id,
                prompt=prompt,
                response=json.dumps(result),
            )
            db.add(entry)
            await db.commit()
        except Exception as e:
            db.rollback()
            print(f"[Companion] Failed to save AI history: {e}")

    return result


async def get_companion_history(db: AsyncSession, user_id: int):
    try:
        stmt = (
            select(AiHistory)
            .where(AiHistory.user_id == user_id)
            .order_by(AiHistory.created_at.asc())
            .limit(10)
        )
        result = await db.execute(stmt)
        entries = result.scalars().all()
        return [
            {
                "prompt": entry.prompt,
                "response": json.loads(entry.response),
                "timestamp": entry.created_at,
            }
            for entry in entries
        ]
    except Exception as e:
        print(f"[Companion History] Error fetching history: {e}")
        return []


async def search_spotify_entities(names, entity_type):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://music-service:8001/spotify/entities",
            params=[("names", n) for n in names] + [("type_", entity_type)],
        )
        response.raise_for_status()
        return response.json()
