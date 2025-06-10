from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc, desc
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserReplace, PasswordChange
from app.core.security import hash_password, verify_password

# User CRUD operations


async def create_user(db: AsyncSession, create_user: UserCreate):
    """Create a new user."""
    hashed_pw = hash_password(create_user.password)
    new_user = User(
        username=create_user.username,
        email=create_user.email,
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_id(db: AsyncSession, user_id: int):
    """Get user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str):
    """Get user by username."""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str):
    """Get user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_all_users(
    db: AsyncSession,
    username: str | None = None,
    email: str | None = None,
    sort: list[str] | None = None,
):
    """Get all users with optional filtering and sorting."""
    query = select(User)
    if username:
        query = query.where(User.username == username)
    if email:
        query = query.where(User.email == email)
    if sort:
        sort_expressions = []
        for field in sort:
            direction = asc
            if field.startswith("-"):
                direction = desc
                field = field[1:]

            sort_column = getattr(User, field, None)
            if sort_column is not None:
                sort_expressions.append(direction(sort_column))
        if sort_expressions:
            query = query.order_by(*sort_expressions)
    else:
        query = query.order_by(User.id.asc())
    result = await db.execute(query)
    return result.scalars().all()


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """Delete user by ID."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False


async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    """Update user partially."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = await result.scalar_one_or_none()

    if not user:
        return None
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email

    await db.commit()
    await db.refresh(user)
    return user


async def replace_user(db: AsyncSession, user_id: int, user_replace: UserReplace):
    """Replace user completely."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = await result.scalar_one_or_none()

    if not user:
        return None

    user.username = user_replace.username
    user.email = user_replace.email

    await db.commit()
    await db.refresh(user)
    return user


async def change_password(db: AsyncSession, payload: PasswordChange, username: str):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user:
        return False
    if not verify_password(payload.current_password, user.hashed_password):
        return False
    user.hashed_password = hash_password(payload.new_password)
    await db.commit()
    await db.refresh(user)
    return True
