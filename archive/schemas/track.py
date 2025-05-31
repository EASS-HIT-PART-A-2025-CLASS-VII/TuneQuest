from pydantic import BaseModel, Field
from typing import Optional


# Base class for shared attributes
class TrackBase(BaseModel):
    title: str = Field(max_length=1000)
    artist: str = Field(max_length=100)
    album: str = Field(max_length=1000)
    genre: str = Field(max_length=50)
    rating: float = Field(ge=0, le=100)


class TrackUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=1000)
    artist: Optional[str] = Field(None, max_length=100)
    album: Optional[str] = Field(None, max_length=1000)
    genre: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(ge=0, le=100)

    class Config:
        from_attributes = True


# For creating a new Track (does not include 'id' because it is generated)
class TrackCreate(TrackBase):
    pass


# for updating all fields in a Track
class TrackReplace(TrackBase):
    pass


# For returning the Track (includes 'id' from DB)
class TrackRead(TrackBase):
    id: int

    class Config:
        from_attributes = True


class TopTrackRead(BaseModel):
    track_id: int
    favorites_count: int
