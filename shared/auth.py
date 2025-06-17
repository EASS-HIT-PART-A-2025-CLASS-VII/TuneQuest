from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional
from dotenv import load_dotenv
import os
from datetime import datetime

class ServiceAuth(HTTPBearer):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.secret_key = os.getenv("SERVICE_SECRET_KEY")
        if not self.secret_key:
            raise ValueError("SERVICE_SECRET_KEY environment variable must be set")

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        
        try:
            token = credentials.credentials
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            if payload.get("service") != "backend":
                raise HTTPException(status_code=403, detail="Invalid service token")
            
            exp = payload.get("exp")
            if exp and exp < datetime.utcnow().timestamp():
                raise HTTPException(status_code=401, detail="Token has expired")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


class PublicAuth(HTTPBearer):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.secret_key = os.getenv("SERVICE_SECRET_KEY")
        if not self.secret_key:
            raise ValueError("SERVICE_SECRET_KEY environment variable must be set")

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        
        try:
            token = credentials.credentials
            # Only verify token signature, don't check service claim
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")