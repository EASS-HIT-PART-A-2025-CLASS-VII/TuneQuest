import pytest
from unittest.mock import AsyncMock, MagicMock
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserUpdate, UserReplace, PasswordChange
from app.models.user import User
from app.core.security import verify_password


@pytest.mark.asyncio
async def test_create_user():
    db = AsyncMock()
    user_data = UserCreate(
        username="testusercreate",
        email="testusercreate@example.com",
        password="strongpass123",
    )

    result = await crud_user.create_user(db, user_data)

    assert result.username == "testusercreate"
    assert result.email == "testusercreate@example.com"
    assert verify_password("strongpass123", result.hashed_password)
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_id():
    db = AsyncMock()
    fake_user = User(
        id=1, username="testuser", email="test@example.com", hashed_password="hashed"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_user
    db.execute.return_value = mock_result

    result = await crud_user.get_user_by_id(db, 1)

    assert result == fake_user
    db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_username():
    db = AsyncMock()
    fake_user = User(
        id=1, username="testuser", email="test@example.com", hashed_password="hashed"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_user
    db.execute.return_value = mock_result

    result = await crud_user.get_user_by_username(db, "testuser")

    assert result == fake_user
    db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_email():
    db = AsyncMock()
    fake_user = User(
        id=1, username="testuser", email="test@example.com", hashed_password="hashed"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_user
    db.execute.return_value = mock_result

    result = await crud_user.get_user_by_email(db, "test@example.com")

    assert result == fake_user
    db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_users():
    db = AsyncMock()
    fake_users = [
        User(
            id=1, username="user1", email="user1@example.com", hashed_password="hashed"
        ),
        User(
            id=2, username="user2", email="user2@example.com", hashed_password="hashed"
        ),
    ]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_users
    db.execute.return_value = mock_result

    result = await crud_user.get_all_users(db)

    assert result == fake_users
    db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_user():
    db = AsyncMock()
    existing_user = User(
        id=1, username="old", email="old@example.com", hashed_password="hashed"
    )
    user_update = UserUpdate(username="new", email="new@example.com")

    result = await crud_user.update_user(db, existing_user.id, user_update)

    assert result.username == "new"
    assert result.email == "new@example.com"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_replace_user():
    db = AsyncMock()
    existing_user = User(
        id=1, username="old", email="old@example.com", hashed_password="hashed"
    )
    user_replace = UserReplace(username="new", email="new@example.com")

    result = await crud_user.replace_user(db, existing_user.id, user_replace)

    assert result.username == "new"
    assert result.email == "new@example.com"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_delete_user():
    db = AsyncMock()

    user = User(
        id=1, username="todelete", email="delete@example.com", hashed_password="hashed"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    db.execute.return_value = mock_result

    result = await crud_user.delete_user(db, user.id)

    assert result is True
    db.delete.assert_called_once_with(user)
    db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_change_password_success():
    db = AsyncMock()

    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password=crud_user.hash_password("oldpassword"),
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    db.execute = AsyncMock(return_value=mock_result)

    password_change = PasswordChange(
        current_password="oldpassword", new_password="newpassword"
    )

    result = await crud_user.change_password(db, password_change, user.username)

    assert result is True
    assert verify_password("newpassword", user.hashed_password)
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_change_password_failure():
    db = AsyncMock()

    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password=crud_user.hash_password("correctpass"),
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    db.execute = AsyncMock(return_value=mock_result)

    password_change = PasswordChange(
        current_password="wrongpass", new_password="newpassword"
    )

    result = await crud_user.change_password(db, password_change, user.username)

    assert result is False
    db.commit.assert_not_called()
    db.refresh.assert_not_called()
