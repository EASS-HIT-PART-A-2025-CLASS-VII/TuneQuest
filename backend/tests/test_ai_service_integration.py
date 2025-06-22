import pytest
from httpx import AsyncClient
import json
from datetime import datetime, timedelta
from app.models.history import AiHistory
from sqlalchemy import select
from app.models.user import User


@pytest.mark.asyncio
async def test_ai_recommend_home_integration(async_client: AsyncClient):
    """
    Tests the /ai/recommend-home endpoint, which typically doesn't require authentication.
    """
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
    response = await async_client.post("/ai/recommend-home", json={"prompt": prompt})

    assert response.status_code == 200
    data = response.json()

    assert "results" in data
    assert isinstance(data["results"], dict)
    assert "tracks" in data["results"]
    assert "artists" in data["results"]
    assert "albums" in data["results"]

    assert isinstance(data["results"]["tracks"], list)
    assert isinstance(data["results"]["artists"], list)
    assert isinstance(data["results"]["albums"], list)

    if data["results"]["tracks"]:
        assert "name" in data["results"]["tracks"][0]
    if data["results"]["artists"]:
        assert "name" in data["results"]["artists"][0]
    if data["results"]["albums"]:
        assert "name" in data["results"]["albums"][0]


@pytest.mark.asyncio
async def test_ai_recommend_button_integration(async_client: AsyncClient):
    """
    Tests the /ai/recommend endpoint, which typically doesn't require authentication.
    """
    request_data = {
        "prompt": """recommend ${type}s similar to ${name}. Return the names only, dont add words. 5 results. Be creative. I want a combination of popular and niche ${type}s. No introductions, no explanations, no other text.""",
        "type": "track",
    }
    response = await async_client.post("/ai/recommend", json=request_data)

    assert response.status_code == 200
    data = response.json()

    assert "results" in data
    assert isinstance(data["results"], list)

    if data["results"]:
        assert "name" in data["results"][0]
        assert data["results"][0]["name"] != "Stairway to Heaven"


@pytest.mark.asyncio
async def test_ai_companion_post_integration(
    async_client: AsyncClient, db_session, create_test_user, get_auth_headers
):
    """
    Tests posting to /ai/companion and verifies the history is saved.
    This test requires a real user and authentication flow.
    """
    username = "ai_post_test_user"
    await create_test_user(username=username, password="testpassword")

    headers = await get_auth_headers(username=username, password="testpassword")

    prompt = "Suggest some relaxing songs for studying."
    response = await async_client.post(
        "/ai/companion", json={"prompt": prompt}, headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "results" in data
    assert isinstance(data["results"], dict)
    assert "tracks" in data["results"]
    assert "artists" in data["results"]
    assert "albums" in data["results"]

    user = (
        (await db_session.execute(select(User).where(User.username == username)))
        .scalars()
        .first()
    )
    assert user is not None

    stmt = select(AiHistory).where(AiHistory.user_id == user.id)
    history_entries = (await db_session.execute(stmt)).scalars().all()

    assert len(history_entries) >= 1
    found_entry = None
    for entry in history_entries:
        if prompt in entry.prompt:
            found_entry = entry
            break

    assert found_entry is not None
    assert found_entry.prompt == prompt
    saved_response = json.loads(found_entry.response)
    assert "results" in saved_response
    assert "tracks" in saved_response["results"]


@pytest.mark.asyncio
async def test_ai_companion_get_history_integration(
    async_client: AsyncClient, db_session, create_test_user, get_auth_headers
):
    """
    Tests retrieving AI companion history for an authenticated user.
    """
    username = "ai_get_test_user"
    await create_test_user(username=username, password="testpassword")

    headers = await get_auth_headers(username=username, password="testpassword")

    from app.models.user import User

    user = (
        (await db_session.execute(select(User).where(User.username == username)))
        .scalars()
        .first()
    )
    assert user is not None

    await db_session.execute(
        AiHistory.__table__.delete().where(AiHistory.user_id == user.id)
    )
    await db_session.commit()

    entry1 = AiHistory(
        user_id=user.id,
        prompt="Integration Test Prompt 1",
        response=json.dumps({"results": {"tracks": [{"name": "Test Track 1"}]}}),
        created_at=datetime.now() - timedelta(minutes=5),
    )
    entry2 = AiHistory(
        user_id=user.id,
        prompt="Integration Test Prompt 2",
        response=json.dumps({"results": {"artists": [{"name": "Test Artist 2"}]}}),
        created_at=datetime.now(),
    )
    db_session.add_all([entry1, entry2])
    await db_session.commit()

    response = await async_client.get("/ai/companion", headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2

    assert data[0]["prompt"] == "Integration Test Prompt 1"
    assert data[1]["prompt"] == "Integration Test Prompt 2"
    assert data[0]["response"]["results"]["tracks"][0]["name"] == "Test Track 1"
    assert data[1]["response"]["results"]["artists"][0]["name"] == "Test Artist 2"
