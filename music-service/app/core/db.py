from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = (
    os.getenv("TEST_DB_URL") if os.getenv("ENV") == "testing" else os.getenv("DB_URL")
)
print(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True, isolation_level="READ COMMITTED")

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
