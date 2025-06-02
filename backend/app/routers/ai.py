from fastapi import APIRouter, HTTPException
import json
from app.schemas.ai import AIRequest, AISpecificRequest
from app.crud.ai_history import (
    get_recommendations_home,
    get_companion,
    get_recommendations_button,
)

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/recommend-home")
def ai_recommend_home(request: AIRequest):
    print(request)
    try:
        result = get_recommendations_home(request.prompt)
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="AI response is not valid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend")
def ai_recommend(request: AISpecificRequest):
    try:
        result = get_recommendations_button(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/companion")
def ai_companion(request: AIRequest):
    try:
        result = get_companion(request.prompt)
        return result

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="AI response is not valid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
