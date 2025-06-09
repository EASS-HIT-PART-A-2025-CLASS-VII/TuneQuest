import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

engine = None
SessionLocal = None


def init_db():
    global engine, SessionLocal

    # Use test database if in testing mode
    if os.getenv("ENV") == "testing":
        DB_URL = os.getenv("TEST_DB_URL")
        poolclass = NullPool  # Disable connection pooling for tests
    else:
        # Try both DB_URL and DATABASE_URL
        DB_URL = os.getenv("DB_URL") or os.getenv("DATABASE_URL")
        poolclass = None

    if not DB_URL:
        raise ValueError(
            "Database URL not configured. Set DB_URL or DATABASE_URL environment variable."
        )

    # Create engine and assign to global variable
    engine = create_async_engine(DB_URL, echo=True, future=True, poolclass=poolclass)

    # Create session maker and assign to global variable
    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    return engine


async def get_db():
    if SessionLocal is None:
        init_db()

    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
