import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import patch
from sqlalchemy import select

from app.crud.ai import (
    get_recommendations_home,
    get_recommendations_button,
    get_companion,
    get_companion_history,
)
from app.schemas.ai import AISpecificRequest
from app.models.history import AiHistory


@pytest.fixture
def sample_ai_response():
    return """```json
{
    "tracks": ["Track A", "Track B"],
    "artists": ["Artist A", "Artist B"],
    "albums": ["Album A", "Album B"]
}
```"""


@pytest.fixture
def cleaned_json_data():
    return {
        "tracks": ["Track A", "Track B"],
        "artists": ["Artist A", "Artist B"],
        "albums": ["Album A", "Album B"],
    }


@pytest.mark.asyncio
@patch("app.crud.ai.ask_gemini")
@patch("app.crud.ai.search_spotify_entities")
async def test_get_recommendations_home(
    mock_search_spotify, mock_ask_gemini, sample_ai_response, cleaned_json_data
):
    mock_ask_gemini.return_value = sample_ai_response

    async def enrich_mock(names, type_):
        return [{"name": f"enriched-{name}"} for name in names]

    mock_search_spotify.side_effect = enrich_mock

    prompt = """
Recommend 10 random tracks, 10 random artists, and 10 random albums.
Return *only* a valid JSON object with exactly 3 keys: "tracks", "artists", and "albums".
Each key must map to an array of names (strings).
No explanations or extra text — only valid JSON.

Example:
{
  "tracks": ["Track 1", "Track 2"],
  "artists": ["Artist 1", "Artist 2"],
  "albums": ["Album 1", "Album 2"]
}
"""

    result = await get_recommendations_home(prompt)

    assert "results" in result
    assert [t["name"] for t in result["results"]["tracks"]] == [
        "enriched-Track A",
        "enriched-Track B",
    ]
    assert [t["name"] for t in result["results"]["albums"]] == [
        "enriched-Album A",
        "enriched-Album B",
    ]
    assert [t["name"] for t in result["results"]["artists"]] == [
        "enriched-Artist A",
        "enriched-Artist B",
    ]


@pytest.mark.asyncio
@patch("app.crud.ai.ask_gemini")
@patch("app.crud.ai.search_spotify_entities")
async def test_get_recommendations_button(mock_search_spotify, mock_ask_gemini):
    ai_response = "- Song 1\n- Song 2\n- Song 3"
    mock_ask_gemini.return_value = ai_response
    enriched_data = [
        {"name": "enriched-Song 1"},
        {"name": "enriched-Song 2"},
        {"name": "enriched-Song 3"},
    ]
    mock_search_spotify.return_value = enriched_data
    prompt = """recommend ${type}s similar to ${name}. Return the names only, dont add words. 5 results. Be creative. I want a combination of popular and niche ${type}s. No introductions, no explanations, no other text."""

    request = AISpecificRequest(prompt=prompt, type="track")
    result = await get_recommendations_button(request)

    assert "results" in result
    assert result["results"] == enriched_data
    mock_search_spotify.assert_called_once_with(["Song 1", "Song 2", "Song 3"], "track")


@pytest.mark.asyncio
@patch("app.crud.ai.ask_gemini")
@patch("app.crud.ai.search_spotify_entities")
async def test_get_companion_success(
    mock_search_spotify, mock_ask_gemini, db_session, create_test_user
):
    ai_text = """```json{"tracks": ["Track X"],"artists": ["Artist Y"],"albums": ["Album Z"]}```"""
    mock_ask_gemini.return_value = ai_text
    mock_search_spotify.side_effect = lambda names, t: [
        {"name": f"enriched-{n}"} for n in names
    ]

    prompt = "test"
    user = await create_test_user("testcompanion123", "securepassword")

    result = await get_companion(db_session, prompt, user_id=user.id)

    assert "results" in result
    assert [t["name"] for t in result["results"]["tracks"]] == ["enriched-Track X"]
    assert [t["name"] for t in result["results"]["artists"]] == ["enriched-Artist Y"]
    assert [t["name"] for t in result["results"]["albums"]] == ["enriched-Album Z"]

    result = await db_session.execute(
        select(AiHistory).where(AiHistory.user_id == user.id)
    )
    entries = result.scalars().all()
    assert len(entries) == 1
    assert prompt in entries[0].prompt


@pytest.mark.asyncio
async def test_get_companion_history_success(db_session, create_test_user):
    user = await create_test_user("testcompanionhistory", "testpassword")

    entry1 = AiHistory(
        user_id=user.id,
        prompt="p1",
        response=json.dumps({"some": "data"}),
        created_at=datetime.now() - timedelta(days=1),
    )
    entry2 = AiHistory(
        user_id=user.id,
        prompt="p2",
        response=json.dumps({"more": "data"}),
        created_at=datetime.now(),
    )

    db_session.add_all([entry1, entry2])
    await db_session.commit()

    result = await get_companion_history(db_session, user_id=user.id)

    assert len(result) == 2
    assert result[0]["prompt"] == "p1"
    assert result[1]["prompt"] == "p2"
    assert isinstance(result[0]["response"], dict)
    assert result[0]["response"]["some"] == "data"
