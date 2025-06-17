import os
import pytest
import asyncio
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport
from app.main import app
from pathlib import Path
from sqlalchemy import MetaData


# Setup test environment
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / ".env.test")
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

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Setup database once for all tests"""
    from app.models.base import Base
    from app.models.favorite import Favorite
    
    # Create a metadata object for music service tables only
    music_metadata = MetaData()
    Favorite.__table__.metadata = music_metadata
    
    async with test_engine.begin() as conn:
        # Drop and create only music service tables
        await conn.run_sync(music_metadata.drop_all)
        await conn.run_sync(music_metadata.create_all)


# Test fixtures
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create database session for test function."""
    session = TestingSessionLocal()
    try:
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
async def backend_client():
    """Create async HTTP client for backend service."""
    from backend.app.main import app as backend_app
    async with AsyncClient(
        transport=ASGITransport(app=backend_app), base_url="http://testserver"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def create_test_user(backend_client):
    """Create test user through backend API."""
    
    async def _create(username: str, password: str):
        response = await backend_client.post(
            "/users/register",
            json={"username": username, "email": f"{username}@example.com", "password": password}
        )
        assert response.status_code == 201
        return response.json()
    
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
