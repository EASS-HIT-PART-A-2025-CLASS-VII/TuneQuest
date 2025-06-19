from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import (
    UserRead,
    UserCreate,
    UserUpdate,
    UserReplace,
    UserLogin,
    PasswordChange,
)
from app.crud.user import (
    create_user,
    get_all_users,
    get_user_by_id,
    get_user_by_username,
    get_user_by_email,
    delete_user,
    update_user,
    replace_user,
    change_password,
)
from app.core.db import get_db
from app.core.auth import create_access_token, get_current_user
from app.core.security import verify_password
from app.models.user import User
from app.constants import user_not_found

# User management router
router = APIRouter(prefix="/users", tags=["users"])

# Valid sort fields for user listing
VALID_SORT_FIELDS = ["id", "username", "email"]


@router.post("/register", response_model=dict)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    existing_email = await get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    user = await create_user(db, user)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=dict)
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = await get_user_by_username(db, user_login.username)
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    """Get current authenticated user."""
    return current_user


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get user by ID."""
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/username/{username}", response_model=UserRead)
async def read_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    """Get user by username."""
    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[UserRead])
async def read_all_users(
    username: str | None = None,
    email: str | None = None,
    sort: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List all users with optional filtering and sorting."""
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
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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


@router.post("/change-password")
async def change_password_endpoint(
    payload: PasswordChange,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = await change_password(db, payload, current_user.username)
    if not success:
        raise HTTPException(status_code=403, detail="Incorrect current password.")
    return {"message": "Password updated successfully"}
