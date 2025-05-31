from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from datetime import datetime, timezone
from enum import Enum as PyEnum
from .base import Base


class FavoriteType(PyEnum):
    track = "track"
    album = "album"
    artist = "artist"


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    spotify_id = Column(String(50), nullable=False)
    type = Column(Enum(FavoriteType), nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
