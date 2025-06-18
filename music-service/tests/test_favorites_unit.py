import pytest
from unittest.mock import AsyncMock, Mock
from app.crud.favorite import create_favorite, get_all_user_favorites, erase_favorite
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_create_favorite_success(mock_db):
    """
    Tests successful creation of a new favorite when it does not exist.
    """
    mock_result = Mock()  # Use a standard Mock for the result object

    # Simulate that the item does NOT exist in the database
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    result = await create_favorite(
        user_id=1,
        spotify_id="abc123",
        db=mock_db,
        type="track",
    )

    assert result is True
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_favorite_duplicate(mock_db):
    """
    Tests that the function returns False if the favorite already exists.
    """
    mock_result = Mock()  # Use a standard Mock

    # Simulate that the item DOES exist in the database
    mock_result.scalar_one_or_none.return_value = object()
    mock_db.execute.return_value = mock_result

    result = await create_favorite(
        user_id=1,
        spotify_id="abc123",
        db=mock_db,
        type="track",
    )

    assert result is False
    mock_db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_create_favorite_missing_type(mock_db):
    """
    Tests that an HTTPException is raised if the 'type' parameter is missing.
    """
    mock_result = Mock()  # Use a standard Mock

    # Simulate that the item does NOT exist, so the function proceeds to the type check
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await create_favorite(
            user_id=1,
            spotify_id="abc1234",
            db=mock_db,
            type=None,  # Pass None for the type
        )

    assert exc_info.value.status_code == 400
    assert "Favorite type is required" in exc_info.value.detail


@pytest.mark.asyncio
async def test_create_favorite_invalid_type(mock_db):
    """
    Tests that an HTTPException is raised for an invalid 'type' string.
    """
    mock_result = Mock()  # Use a standard Mock

    # Simulate that the item does NOT exist
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await create_favorite(
            user_id=1,
            spotify_id="abc12345",
            db=mock_db,
            type="playlist",  # An invalid type
        )

    assert exc_info.value.status_code == 400
    assert "Invalid favorite type" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_all_user_favorites():
    """
    Tests retrieving all favorites for a specific user.
    """
    mock_db = AsyncMock()
    mock_favorite = Mock()
    mock_favorite.user_id = 1
    mock_favorite.spotify_id = "abc123"
    mock_favorite.type = "track"

    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = [mock_favorite]
    mock_db.execute.return_value = mock_result

    result = await get_all_user_favorites(1, mock_db)

    assert len(result) == 1
    assert result[0].user_id == 1
    assert result[0].spotify_id == "abc123"
    assert result[0].type == "track"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_erase_favorite_success(mock_db):
    """
    Tests successfully erasing a favorite that exists.
    """
    mock_result = Mock()
    mock_favorite = Mock()
    mock_favorite.user_id = 1
    mock_favorite.spotify_id = "abc123"
    mock_favorite.type = "track"
    mock_result.scalar_one_or_none.return_value = mock_favorite
    mock_db.execute.return_value = mock_result

    result = await erase_favorite(1, "abc123", mock_db, "track")

    assert result is True
    mock_db.commit.assert_called_once()
    mock_db.delete.assert_called_once_with(mock_favorite)


@pytest.mark.asyncio
async def test_erase_favorite_not_found(mock_db):
    """
    Tests attempting to erase a favorite that doesn't exist.
    """
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    result = await erase_favorite(1, "abc123", mock_db, "track")

    assert result is False
    mock_db.commit.assert_not_called()
    mock_db.delete.assert_not_called()


@pytest.mark.asyncio
async def test_erase_favorite_invalid_type(mock_db):
    """
    Tests attempting to erase a favorite with an invalid type.
    """
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await erase_favorite(1, "abc123", mock_db, "invalid_type")

    assert exc_info.value.status_code == 400
    assert "Invalid favorite type" in exc_info.value.detail
    mock_db.commit.assert_not_called()
    mock_db.delete.assert_not_called()
