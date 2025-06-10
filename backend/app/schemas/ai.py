from pydantic import BaseModel
from typing import Optional

# AI schemas


class AISpecificRequest(BaseModel):
    """Specific AI request schema."""

    prompt: str
    type: str


class AIRequest(BaseModel):
    """AI request schema."""

    prompt: str
    user_id: Optional[int] = None
