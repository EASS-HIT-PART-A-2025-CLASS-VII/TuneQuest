from datetime import datetime, timedelta, timezone
from authlib.jose import jwt
from authlib.jose.errors import JoseError
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import User
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Argon2 password context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {**data, "exp": expire}
    encoded_jwt = jwt.encode({"alg": ALGORITHM}, to_encode, SECRET_KEY)

    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    print(f"Token received: {token}")

    try:
        payload = jwt.decode(token, SECRET_KEY, claims_options={"alg": ALGORITHM})
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )

        result = await db.execute(select(User).filter(User.username == username))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JoseError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
