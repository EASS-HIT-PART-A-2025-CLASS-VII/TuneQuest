from pydantic import BaseModel
from typing import Optional


# Base class for shared attributes
class TrackBase(BaseModel):
    title: str
    artist: str
    album: str
    genre: str
    rating: float


class TrackUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    rating: Optional[float] = None

    class Config:
        orm_mode = True


# For creating a new Track (does not include 'id' because it is generated)
class TrackCreate(TrackBase):
    pass


# for updating all fields in a Track
class TrackReplace(TrackBase):
    pass


# For returning the Track (includes 'id' from DB)
class Track(TrackBase):
    id: int

    class Config:
        orm_mode = True
