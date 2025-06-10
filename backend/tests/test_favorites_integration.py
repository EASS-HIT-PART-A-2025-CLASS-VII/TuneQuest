import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.favorite import (
    create_favorite,
    get_all_user_favorites,
    erase_favorite,
)
from app.models.favorite import FavoriteType

import asyncio
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_favorite_lifecycle(db_session: AsyncSession, create_test_user):
    """Test complete favorite lifecycle."""
    test_user = await create_test_user("testuser", "password")
    spotify_id = "test_track_123"

    # Create favorite
    create_result = await create_favorite(
        user_id=test_user.id,
        spotify_id=spotify_id,
        db=db_session,
        type="track",
    )
    assert create_result is True

    # Get favorites
    favorites = await get_all_user_favorites(test_user.id, db_session)
    assert len(favorites) == 1
    favorite = favorites[0]
    assert favorite.user_id == test_user.id
    assert favorite.spotify_id == spotify_id
    assert favorite.type == FavoriteType.track

    # Delete favorite
    delete_result = await erase_favorite(
        user_id=test_user.id,
        spotify_id=spotify_id,
        db=db_session,
        type="track",
    )
    assert delete_result is True

    # Verify deletion
    favorites_after_delete = await get_all_user_favorites(test_user.id, db_session)
    assert len(favorites_after_delete) == 0


@pytest.mark.asyncio
@patch("app.crud.favorite.get_albums_by_ids")
@patch("app.crud.favorite.get_artists_by_ids")
@patch("app.crud.favorite.get_tracks_by_ids")
async def test_favorite_with_metadata(
    mock_get_albums,
    mock_get_artists,
    mock_get_tracks,
    db_session: AsyncSession,
    create_test_user,
):
    """Test favorite operations with Spotify metadata."""
    test_user = await create_test_user("testuser_metadata", "password")
    spotify_id = "test_track_123"

    # Mock Spotify API responses
    mock_get_tracks.return_value = AsyncMock(
        return_value=[{"name": "Test Track", "artists": [{"name": "Test Artist"}]}]
    )
    mock_get_artists.return_value = AsyncMock(
        return_value=[{"name": "Test Artist", "genres": ["rock"]}]
    )
    mock_get_albums.return_value = AsyncMock(
        return_value=[{"name": "Test Album", "images": [{"url": "test_url"}]}]
    )

    # Create favorite
    create_result = await create_favorite(
        user_id=test_user.id,
        spotify_id=spotify_id,
        db=db_session,
        type="track",
    )
    assert create_result is True

    # Get favorites with metadata
    favorites = await get_all_user_favorites(test_user.id, db_session)
    assert len(favorites) == 1
    favorite = favorites[0]
    assert favorite.user_id == test_user.id
    assert favorite.spotify_id == spotify_id
    assert favorite.type == FavoriteType.track

    # Delete favorite
    delete_result = await erase_favorite(
        user_id=test_user.id,
        spotify_id=spotify_id,
        db=db_session,
        type="track",
    )
    assert delete_result is True

    # Verify deletion
    favorites_after_delete = await get_all_user_favorites(test_user.id, db_session)
    assert len(favorites_after_delete) == 0


@pytest.mark.asyncio
async def test_concurrent_operations(db_sessions: list[AsyncSession], create_test_user):
    """Test concurrent favorite operations."""
    test_user = await create_test_user("testuser_concurrent", "password")

    # Create favorites concurrently
    create_tasks = []
    for i in range(5):
        task = asyncio.create_task(
            create_favorite(
                user_id=test_user.id,
                spotify_id=f"track_{i}",
                db=db_sessions[i],
                type="track",
            )
        )
        create_tasks.append(task)

    create_results = await asyncio.gather(*create_tasks)
    assert all(create_results)

    # Verify favorites
    favorites = await get_all_user_favorites(test_user.id, db_sessions[0])
    assert len(favorites) == 5

    # Delete favorites concurrently
    delete_tasks = []
    for i in range(5):
        task = asyncio.create_task(
            erase_favorite(
                user_id=test_user.id,
                spotify_id=f"track_{i}",
                db=db_sessions[i],
                type="track",
            )
        )
        delete_tasks.append(task)

    delete_results = await asyncio.gather(*delete_tasks)
    assert all(delete_results)

    # Verify deletion
    favorites_after_delete = await get_all_user_favorites(test_user.id, db_sessions[0])
    assert len(favorites_after_delete) == 0
