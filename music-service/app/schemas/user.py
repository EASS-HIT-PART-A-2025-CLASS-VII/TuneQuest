from pydantic import BaseModel
from app.models.user import User

class User(BaseModel):
    id: int