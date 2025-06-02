from pydantic import BaseModel


class AISpecificRequest(BaseModel):
    prompt: str
    type: str


class AIRequest(BaseModel):
    prompt: str
