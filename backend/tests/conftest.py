import os
import pytest
import asyncio
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.models.user import User
from app.core.security import hash_password
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.db import init_db
from pathlib import Path
from sqlalchemy import MetaData, text
from unittest.mock import AsyncMock
from app.crud import user as crud_user


# Setup test environment
BACKEND_DIR = Path(__file__).parent.parent
load_dotenv(BACKEND_DIR / ".env.test")
os.environ["ENV"] = "testing"

# Database setup
TEST_DB_URL = os.getenv("TEST_DB_URL")
test_engine = create_async_engine(
    TEST_DB_URL,
    echo=True,
    future=True,
    poolclass=NullPool,
)
print(f"Using test DB URL: {TEST_DB_URL}")

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Test fixtures
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Setup database once for all tests"""
    from app.models.base import Base
    from app.models.user import User
    from app.models.history import AiHistory
    
    # Clean tables before tests start
    async with TestingSessionLocal() as session:
        await session.begin()
        await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
        await session.execute(text("TRUNCATE TABLE ai_history RESTART IDENTITY CASCADE"))
        await session.commit()

    yield

    # Clean tables after all tests
    async with TestingSessionLocal() as session:
        await session.begin()
        await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
        await session.execute(text("TRUNCATE TABLE ai_history RESTART IDENTITY CASCADE"))
        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create database session for test function."""
    session = TestingSessionLocal()
    try:
        # Clean tables before each test
        await session.begin()
        yield session
    finally:
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture
async def db_sessions():
    """Create multiple database sessions for concurrent tests."""
    sessions = []
    for _ in range(5):
        session = TestingSessionLocal()
        await session.begin()
        sessions.append(session)

    try:
        yield sessions
    finally:
        for session in sessions:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture
async def async_client():
    """Create async HTTP client for testing."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def mock_db():
    """Create a mock database session for unit tests."""
    db = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock()
    return db


@pytest_asyncio.fixture
async def create_test_user(db_session):
    """Create test user."""

    async def _create(username: str, password: str):
        user = User(
            username=username,
            email=f"{username}@example.com",
            hashed_password=hash_password(password),
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    return _create


@pytest_asyncio.fixture
async def get_auth_headers(async_client):
    async def _headers(username: str, password: str):
        response = await async_client.post(
            "/users/login", json={"username": username, "password": password}
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _headers
