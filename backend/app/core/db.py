import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

engine = None
SessionLocal = None

def init_db():
    """Initialize database connection with proper configuration."""
    global engine, SessionLocal

    if os.getenv("ENV") == "testing":
        DB_URL = os.getenv("TEST_DB_URL")
        print(DB_URL)
        poolclass = NullPool  # Disable pooling for tests
    else:
        DB_URL = os.getenv("DB_URL")
        print(DB_URL)
        poolclass = None

    if not DB_URL:
        raise ValueError("Database URL not configured")

    engine = create_async_engine(DB_URL, echo=True, future=True, poolclass=poolclass)
    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    return engine


async def get_db():
    """Get database session for dependency injection."""
    if SessionLocal is None:
        init_db()

    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
