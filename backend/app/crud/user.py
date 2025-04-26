from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserReplace
from sqlalchemy import asc, desc


async def create_user(db: AsyncSession, create_user: UserCreate):
    user = User(**create_user.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_all_users(
    db: AsyncSession,
    username: str | None = None,
    email: str | None = None,
    sort: list[str] | None = None,
):
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
        query = query.order_by(User.id.asc)
    result = await db.execute(query)
    return result.scalars().all()


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False


async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

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
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        return None

    user.username = user_replace.username
    user.email = user_replace.email

    await db.commit()
    await db.refresh(user)
    return user
