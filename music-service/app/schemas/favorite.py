from pydantic import BaseModel, ConfigDict
from app.models.favorite import FavoriteType

# Favorite schemas


class FavoriteBase(BaseModel):
    """Base favorite schema."""

    user_id: int
    spotify_id: str
    type: FavoriteType


class FavoriteCreate(FavoriteBase):
    """Create favorite schema."""

    pass


class FavoriteRead(FavoriteBase):
    """Read favorite schema."""

    id: int
    model_config = ConfigDict(from_attributes=True)
