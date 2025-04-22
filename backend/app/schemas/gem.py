from pydantic import BaseModel
from typing import Optional

# Base class for shared attributes
class GemBase(BaseModel):
    name: str
    location: str
    description: str
    rating: float
    category: str

# For creating a new gem (does not include 'id' because it is generated)
class GemCreate(GemBase):
    pass

# For returning the gem (includes 'id' from DB)
class Gem(GemBase):
    id: int

    class Config:
        orm_mode = True  # This makes Pydantic models compatible with SQLAlchemy models
