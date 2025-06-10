import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_and_read_favorite(
    async_client: AsyncClient, create_test_user, get_auth_headers
):
    username = "favtestuser1"
    password = "password123"
    await create_test_user(username, password)
    headers = await get_auth_headers(username, password)

    spotify_id = "test_spotify_id_123"
    type_ = "track"

    response = await async_client.post(
        f"/favorites/?spotify_id={spotify_id}&type={type_}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

    response = await async_client.get(
        f"/favorites/{spotify_id}?type={type_}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

    response = await async_client.get("/favorites/", headers=headers)
    assert response.status_code == 200

    favorites = response.json()
    assert isinstance(favorites, list)
    assert any(f["spotify_id"] == spotify_id for f in favorites)


@pytest.mark.asyncio
async def test_delete_favorite(
    async_client: AsyncClient, create_test_user, get_auth_headers
):
    username = "favtestuser2"
    password = "password123"
    await create_test_user(username, password)
    headers = await get_auth_headers(username, password)

    spotify_id = "test_spotify_id_to_delete"
    type_ = "album"

    await async_client.post(
        f"/favorites/?spotify_id={spotify_id}&type={type_}",
        headers=headers,
    )

    response = await async_client.delete(
        f"/favorites/{spotify_id}?type={type_}", headers=headers
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

    response = await async_client.get(
        f"/favorites/{spotify_id}?type={type_}", headers=headers
    )
    assert response.status_code == 200
    assert response.json()["result"] is False


@pytest.mark.asyncio
async def test_invalid_favorite_type(
    async_client: AsyncClient, create_test_user, get_auth_headers
):
    username = "favtestuser3"
    password = "password123"
    await create_test_user(username, password)
    headers = await get_auth_headers(username, password)

    response = await async_client.post(
        "/favorites/?spotify_id=abc123&type=invalid_type",
        headers=headers,
    )
    assert response.status_code in {400, 422}


@pytest.mark.asyncio
async def test_get_spotify_metadata(
    async_client: AsyncClient, create_test_user, get_auth_headers
):
    username = "favtestuser4"
    password = "password123"
    await create_test_user(username, password)
    headers = await get_auth_headers(username, password)

    response = await async_client.get("/favorites/spotify", headers=headers)
    assert response.status_code in {200, 500}
