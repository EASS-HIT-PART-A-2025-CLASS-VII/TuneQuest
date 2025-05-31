from pydantic import BaseModel
from app.models.favorite import FavoriteType


class FavoriteBase(BaseModel):
    user_id: int
    spotify_id: str
    type: FavoriteType


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteRead(FavoriteBase):
    id: int

    class Config:
        from_attributes = True
