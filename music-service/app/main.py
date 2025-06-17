from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    user_favorites,
    spotify,
    deezer,
)
from app.services import deezer_genres
from app.core.db import engine
from contextlib import asynccontextmanager


app = FastAPI(
    title="TuneQuest Music Service",
    description="Microservice handling all music-related operations",
    version="1.0.0"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    deezer_genres.load_deezer_genres()
    yield
    
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(user_favorites.router)
app.include_router(spotify.router)
app.include_router(deezer.router)
