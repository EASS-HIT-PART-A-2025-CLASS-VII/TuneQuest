import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(create_test_user):
    """Test user registration."""
    response = await create_test_user("test_user", "securepassword")
    assert response.username == "test_user"

@pytest.mark.asyncio
async def test_register_duplicate_user(async_client: AsyncClient, create_test_user):
    """Test duplicate user registration."""
    # First create a user
    await create_test_user("test_user_duplicate", "securepassword")
    
    # Try to create the same user again
    response = await async_client.post(
        "/users/register",
        json={
            "username": "test_user_duplicate",
            "email": "test@example.com",
            "password": "securepassword",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"

@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    """Test user login."""
    await async_client.post(
        "/users/register",
        json={
            "username": "login_user",
            "email": "login@example.com",
            "password": "securepassword",
        },
    )
    response = await async_client.post(
        "/users/login", json={"username": "login_user", "password": "securepassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client: AsyncClient):
    """Test login with invalid credentials."""
    await async_client.post(
        "/users/register",
        json={
            "username": "invalid_login_user",
            "email": "invalid@example.com",
            "password": "correctpassword",
        },
    )
    response = await async_client.post(
        "/users/login", json={"username": "invalid_login_user", "password": "wrongpassword"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user(async_client: AsyncClient):
    """Test getting current user."""
    await async_client.post(
        "/users/register",
        json={
            "username": "current_user",
            "email": "current@example.com",
            "password": "securepassword",
        },
    )
    login_response = await async_client.post(
        "/users/login", json={"username": "current_user", "password": "securepassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "current_user"

@pytest.mark.asyncio
async def test_register_invalid_username(async_client: AsyncClient):
    """Test registration with invalid usernames."""
    invalid_usernames = ["", "ab", "a" * 21]
    for username in invalid_usernames:
        response = await async_client.post(
            "/users/register",
            json={
                "username": username,
                "email": "valid@example.com",
                "password": "securepassword",
            },
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_invalid_email(async_client: AsyncClient):
    invalid_emails = ["not-an-email", "missing-at-sign.com", "missingdomain@.com"]
    for email in invalid_emails:
        response = await async_client.post(
            "/users/register",
            json={
                "username": "validusername",
                "email": email,
                "password": "securepassword",
            },
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_invalid_password_length(async_client: AsyncClient):
    invalid_passwords = ["short", "a" * 21]
    for pwd in invalid_passwords:
        response = await async_client.post(
            "/users/register",
            json={
                "username": "validusername",
                "email": "valid@example.com",
                "password": pwd,
            },
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_change_password_success(
    async_client: AsyncClient, create_test_user, get_auth_headers
):
    await create_test_user(username="change_pass_user", password="oldpassword123")
    headers = await get_auth_headers(username="change_pass_user", password="oldpassword123")

    response = await async_client.post(
        "/users/change-password",
        json={
            "current_password": "oldpassword123",
            "new_password": "newsecurepassword456",
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"


@pytest.mark.asyncio
async def test_login_after_password_change(
    async_client: AsyncClient, create_test_user, get_auth_headers
):
    await create_test_user(username="login_after_pass_change_user", password="oldpass123")
    headers = await get_auth_headers(username="login_after_pass_change_user", password="oldpass123")

    response = await async_client.post(
        "/users/change-password",
        json={"current_password": "oldpass123", "new_password": "newpass456"},
        headers=headers,
    )
    assert response.status_code == 200

    login_response = await async_client.post(
        "/users/login", json={"username": "login_after_pass_change_user", "password": "newpass456"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


@pytest.mark.asyncio
async def test_change_password_incorrect_current(
    async_client: AsyncClient, create_test_user, get_auth_headers
):
    await create_test_user(username="wrong_pass_user", password="correct_pass")
    headers = await get_auth_headers(username="wrong_pass_user", password="correct_pass")

    response = await async_client.post(
        "/users/change-password",
        json={"current_password": "wrong_pass", "new_password": "new_pass"},
        headers=headers,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Incorrect current password."


@pytest.mark.asyncio
async def test_change_password_unauthenticated(async_client: AsyncClient):
    response = await async_client.post(
        "/users/change-password",
        json={"current_password": "doesntmatter", "new_password": "irrelevant"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"current_password": "", "new_password": "new"},
        {"current_password": "current", "new_password": ""},
        {"current_password": "", "new_password": ""},
    ],
)
async def test_change_password_validation(
    async_client: AsyncClient, create_test_user, get_auth_headers, payload
):
    username = f"valtest_{hash(str(payload))}"
    await create_test_user(username=username, password="valid_pass")
    headers = await get_auth_headers(username=username, password="valid_pass")

    response = await async_client.post(
        "/users/change-password", json=payload, headers=headers
    )

    assert response.status_code == 422
