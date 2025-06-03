from pydantic import BaseModel
from typing import Optional


class AISpecificRequest(BaseModel):
    prompt: str
    type: str


class AIRequest(BaseModel):
    prompt: str
    user_id: Optional[int] = None
