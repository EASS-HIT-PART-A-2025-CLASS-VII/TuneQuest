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

# Setup test environment
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / ".env.test")
os.environ["ENV"] = "testing"
init_db()

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


@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables():
    """Create and drop tables for each test function."""
    from app.models.base import Base

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Cleanup after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    """Create test database tables."""
    from app.models.base import Base

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


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
