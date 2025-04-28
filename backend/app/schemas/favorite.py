from pydantic import BaseModel


class FavoriteBase(BaseModel):
    user_id: int
    track_id: int


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteRead(FavoriteBase):
    id: int

    class Config:
        from_attributes = True
