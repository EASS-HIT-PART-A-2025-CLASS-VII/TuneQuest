import pytest
from unittest.mock import MagicMock
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserUpdate, UserReplace, PasswordChange
from app.models.user import User
from app.core.security import verify_password


@pytest.mark.asyncio
async def test_create_user(mock_db):
    user_data = UserCreate(
        username="test_user_create",
        email="test_user_create@example.com",
        password="strong_pass_123",
    )

    result = await crud_user.create_user(mock_db, user_data)

    assert result.username == "test_user_create"
    assert result.email == "test_user_create@example.com"
    assert verify_password("strong_pass_123", result.hashed_password)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_id(mock_db):
    fake_user = User(
        id=1, username="test_user_id", email="test_user_id@example.com", hashed_password="hashed"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_user
    mock_db.execute.return_value = mock_result

    result = await crud_user.get_user_by_id(mock_db, 1)

    assert result == fake_user
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_username(mock_db):
    fake_user = User(
        id=1, username="test_user_username", email="test_user_username@example.com", hashed_password="hashed"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_user
    mock_db.execute.return_value = mock_result

    result = await crud_user.get_user_by_username(mock_db, "test_user_username")

    assert result == fake_user
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_email(mock_db):
    fake_user = User(
        id=1, username="test_user_email", email="test_user_email@example.com", hashed_password="hashed"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_user
    mock_db.execute.return_value = mock_result

    result = await crud_user.get_user_by_email(mock_db, "test_user_email@example.com")

    assert result == fake_user
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_users(mock_db):
    fake_users = [
        User(
            id=1, username="test_user_1", email="test_user_1@example.com", hashed_password="hashed"
        ),
        User(
            id=2, username="test_user_2", email="test_user_2@example.com", hashed_password="hashed"
        ),
    ]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_users
    mock_db.execute.return_value = mock_result

    result = await crud_user.get_all_users(mock_db)

    assert result == fake_users
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_user(mock_db):
    existing_user = User(
        id=1, username="test_user_old", email="test_user_old@example.com", hashed_password="hashed"
    )
    user_update = UserUpdate(username="new", email="new@example.com")

    result = await crud_user.update_user(mock_db, existing_user.id, user_update)

    assert result.username == "new"
    assert result.email == "new@example.com"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_replace_user(mock_db):
    existing_user = User(
        id=1, username="test_user_old", email="test_user_old@example.com", hashed_password="hashed"
    )
    user_replace = UserReplace(username="new", email="new@example.com")

    result = await crud_user.replace_user(mock_db, existing_user.id, user_replace)

    assert result.username == "new"
    assert result.email == "new@example.com"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_delete_user(mock_db):
    user = User(
        id=1, username="test_user_delete", email="test_user_delete@example.com", hashed_password="hashed"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_db.execute.return_value = mock_result

    result = await crud_user.delete_user(mock_db, user.id)

    assert result is True
    mock_db.delete.assert_called_once_with(user)
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_change_password_success(mock_db):
    user = User(
        id=1,
        username="test_user_change_password_success",
        email="test_user_change_password_success@example.com",
        hashed_password=crud_user.hash_password("old_password"),
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_db.execute.return_value = mock_result

    password_change = PasswordChange(
        current_password="old_password", new_password="new_password"
    )

    result = await crud_user.change_password(mock_db, password_change, user.username)

    assert result is True
    assert verify_password("new_password", user.hashed_password)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_change_password_failure(mock_db):
    user = User(
        id=1,
        username="test_user_change_password_failure",
        email="test_user_change_password_failure@example.com",
        hashed_password=crud_user.hash_password("correct_pass"),
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_db.execute.return_value = mock_result

    password_change = PasswordChange(
        current_password="wrong_pass", new_password="new_password"
    )

    result = await crud_user.change_password(mock_db, password_change, user.username)

    assert result is False
    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()
