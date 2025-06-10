import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.favorite import (
    create_favorite,
    get_all_user_favorites,
    erase_favorite,
    get_spotify_metadata_for_user_favorites,
)
from app.models.favorite import Favorite, FavoriteType
from app.models.user import User
import asyncio
from unittest.mock import AsyncMock, patch


# @pytest.mark.asyncio
# async def test_full_favorite_flow(
#     db_session: AsyncSession,
#     create_test_user
# ):
#     # Create test user using fixture
#     test_user = await create_test_user("testuser", "password")

#     # Create a favorite
#     create_result = await create_favorite(
#         user_id=test_user.id,
#         spotify_id="test_track_123",
#         db=db_session,
#         type="track",
#     )
#     assert create_result is True

#     # Get all user favorites and verify it exists
#     favorites = await get_all_user_favorites(test_user.id, db_session)
#     assert len(favorites) == 1
#     favorite = favorites[0]
#     assert favorite.user_id == test_user.id
#     assert favorite.spotify_id == "test_track_123"
#     assert favorite.type == FavoriteType.track

#     # Delete the favorite
#     delete_result = await erase_favorite(
#         user_id=test_user.id,
#         spotify_id="test_track_123",
#         db=db_session,
#         type="track",
#     )
#     assert delete_result is True

#     # Verify it's deleted
#     favorites_after_delete = await get_all_user_favorites(test_user.id, db_session)
#     assert len(favorites_after_delete) == 0
#     """
#     Integration test that verifies the complete flow of favorite operations:
#     create -> get -> delete
#     """
#     # Create a favorite
#     create_result = await create_favorite(
#         user_id=1,
#         spotify_id="test_track_123",
#         db=db_session,
#         type="track",
#     )
#     assert create_result is True

#     # Get all user favorites and verify it exists
#     favorites = await get_all_user_favorites(1, db_session)
#     assert len(favorites) == 1
#     favorite = favorites[0]
#     assert favorite.user_id == 1
#     assert favorite.spotify_id == "test_track_123"
#     assert favorite.type == FavoriteType.track

#     # Delete the favorite
#     delete_result = await erase_favorite(
#         user_id=1,
#         spotify_id="test_track_123",
#         db=db_session,
#         type="track",
#     )
#     assert delete_result is True

#     # Verify it's deleted
#     favorites_after_delete = await get_all_user_favorites(1, db_session)
#     assert len(favorites_after_delete) == 0


# @pytest.mark.asyncio
# @patch("app.crud.favorite.get_albums_by_ids")
# @patch("app.crud.favorite.get_artists_by_ids")
# @patch("app.crud.favorite.get_tracks_by_ids")
# async def test_favorite_lifecycle_with_metadata(
#     mock_get_albums,
#     mock_get_artists,
#     mock_get_tracks,
#     db_session: AsyncSession,
#     create_test_user,
# ):
#     # Create test user using fixture
#     test_user = await create_test_user("testuser_metadata", "password")

#     # Mock Spotify API responses
#     def mock_tracks(ids):
#         print(f"\nTracks mock called with IDs: {ids}")
#         return [{"id": id, "name": f"Track {id}", "artists": [{"name": "Test Artist"}]} for id in ids]

#     def mock_albums(ids):
#         print(f"\nAlbums mock called with IDs: {ids}")
#         return [{"id": id, "name": f"Album {id}", "artists": [{"name": "Test Artist"}]} for id in ids]

#     def mock_artists(ids):
#         print(f"\nArtists mock called with IDs: {ids}")
#         return [{"id": id, "name": f"Artist {id}"} for id in ids]

#     mock_get_tracks.side_effect = mock_tracks
#     mock_get_albums.side_effect = mock_albums
#     mock_get_artists.side_effect = mock_artists

#     print("\n=== Starting test ===")

#     # Create multiple favorites of different types
#     favorites = []
#     for spotify_id, fav_type in [
#         ("track_123", "track"),
#         ("album_456", "album"),
#         ("artist_789", "artist"),
#     ]:
#         result = await create_favorite(
#             user_id=test_user.id,
#             spotify_id=spotify_id,
#             db=db_session,
#             type=fav_type,
#         )
#         assert result is True
#         favorites.append((spotify_id, fav_type))

#     # Get metadata for all user favorites
#     metadata = await get_spotify_metadata_for_user_favorites(test_user.id, db_session)
#     assert len(metadata) == 3

#     # Verify we got metadata for each favorite type
#     assert len(metadata["tracks"]) == 1
#     assert len(metadata["albums"]) == 1
#     assert len(metadata["artists"]) == 1

#     # Verify each favorite has the correct metadata
#     assert metadata["tracks"][0]["id"] == "track_123"
#     assert metadata["albums"][0]["id"] == "album_456"
#     assert metadata["artists"][0]["id"] == "artist_789"

#     # Clean up by deleting all favorites
#     for spotify_id, fav_type in favorites:
#         result = await erase_favorite(
#             user_id=test_user.id,
#             spotify_id=spotify_id,
#             db=db_session,
#             type=fav_type,
#         )
#         assert result is True

#     # Verify all favorites are deleted
#     favorites_after_delete = await get_all_user_favorites(test_user.id, db_session)
#     assert len(favorites_after_delete) == 0


@pytest.mark.asyncio
async def test_concurrent_operations(db_sessions: list[AsyncSession], create_test_user):
    # Create test user using fixture
    test_user = await create_test_user("testuser_concurrent", "password")

    # Create multiple favorites concurrently with separate sessions
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

    # Get all favorites and verify count
    favorites = await get_all_user_favorites(test_user.id, db_sessions[0])
    assert len(favorites) == 5

    # Delete favorites concurrently with separate sessions
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

    # Verify all favorites are deleted
    favorites_after_delete = await get_all_user_favorites(test_user.id, db_sessions[0])
    assert len(favorites_after_delete) == 0
