from pydantic import BaseModel


class FavoriteBase(BaseModel):
    user_id: int
    spotify_track_id: str


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteRead(FavoriteBase):
    id: int

    class Config:
        from_attributes = True
