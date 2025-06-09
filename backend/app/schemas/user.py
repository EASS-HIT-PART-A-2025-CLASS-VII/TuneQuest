from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=20)


class UserReplace(UserBase):
    pass


class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=20)
