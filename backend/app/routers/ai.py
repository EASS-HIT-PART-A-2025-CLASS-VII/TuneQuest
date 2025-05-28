from fastapi import APIRouter, HTTPException
from app.services.ai import ask_gemini
from app.services.spotify_search import search_spotify_entities
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["ai"])


class AIRequest(BaseModel):
    prompt: str
    type: str


@router.post("/recommend")
def ai_recommend(request: AIRequest):
    try:
        ai_response = ask_gemini(request.prompt)

        names = [
            line.strip("- ").strip()
            for line in ai_response.strip().splitlines()
            if line.strip()
        ]

        enriched = search_spotify_entities(names, request.type)
        print(enriched)
        return {"results": enriched}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
