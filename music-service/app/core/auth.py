# music-service/app/core/auth.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import User 
from app.core.db import get_db

async def get_current_user(db: AsyncSession = Depends(get_db)):
    """Get current user from token (backend handles the actual auth)"""
    # For now, we'll just return a dummy user since we're not implementing full auth
    # In production, this would validate the token and get user info from backend
    return User(id=1)  