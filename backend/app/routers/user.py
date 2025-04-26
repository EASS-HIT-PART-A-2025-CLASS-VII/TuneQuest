from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserRead, UserCreate, UserUpdate, UserReplace
from app.crud.user import (
    create_user,
    get_all_users,
    get_user,
    delete_user,
    update_user,
    replace_user,
)
from app.core.db import SessionLocal


router = APIRouter(prefix="/users", tags=["users"])
user_not_found = "User not found"
VALID_SORT_FIELDS = ["id", "username", "email"]


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/", response_model=UserRead)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=user_not_found)
    return user


@router.get("/", response_model=list[UserRead])
async def read_all_users(
    username: str | None = None,
    email: str | None = None,
    sort: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    validated_sort = []
    if sort:
        fields = sort.split(",")
        for field in fields:
            clean_field = field.lstrip("-")
            if clean_field not in VALID_SORT_FIELDS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid sort field: {clean_field}. Choose from: {', '.join(VALID_SORT_FIELDS)}",
                )
        validated_sort = fields

    return await get_all_users(db, username, email, validated_sort)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail=user_not_found)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_endpoint(
    user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)
):
    updated_user = await update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail=user_not_found)
    return updated_user


@router.put("/{user_id}", response_model=UserRead)
async def replace_user_endpoint(
    user_id: int, user_replace: UserReplace, db: AsyncSession = Depends(get_db)
):
    replaced_user = await replace_user(db, user_id, user_replace)
    if not replaced_user:
        raise HTTPException(status_code=404, detail=user_not_found)
    return replaced_user
