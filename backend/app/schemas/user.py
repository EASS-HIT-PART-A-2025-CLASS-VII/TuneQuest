from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

# User schemas


class UserBase(BaseModel):
    """Base user schema."""

    username: str = Field(min_length=3, max_length=20)
    email: EmailStr


class UserCreate(UserBase):
    """Create user schema."""

    password: str = Field(min_length=8, max_length=20)


class UserUpdate(BaseModel):
    """Update user schema."""

    username: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None


class UserReplace(UserBase):
    """Replace user schema."""

    pass


class UserRead(UserBase):
    """Read user schema."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Login schema."""

    username: str
    password: str


class PasswordChange(BaseModel):
    """Password change schema."""

    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=20)
