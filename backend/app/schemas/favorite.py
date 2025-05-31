from pydantic import BaseModel
from typing import Literal


class FavoriteBase(BaseModel):
    user_id: int
    spotify_id: str
    type: Literal["track", "album", "artist"]


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteRead(FavoriteBase):
    id: int

    class Config:
        from_attributes = True
