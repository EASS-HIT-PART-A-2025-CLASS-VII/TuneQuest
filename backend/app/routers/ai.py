from fastapi import APIRouter, HTTPException
import json
from app.schemas.ai import AIRequest, AISpecificRequest
from app.crud.ai import (
    get_recommendations_home,
    get_companion,
    get_recommendations_button,
    get_companion_history,
)
from fastapi import Depends
from app.core.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.models.user import User

# AI endpoints
router = APIRouter(prefix="/ai", tags=["ai"])
ai_response_is_not_valid = "AI response is not valid JSON"


@router.post("/recommend-home")
async def ai_recommend_home(request: AIRequest):
    """Get AI home recommendations."""
    try:
        result = await get_recommendations_home(request.prompt)
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid AI response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend")
async def ai_recommend(request: AISpecificRequest):
    """Get specific AI recommendations."""
    try:
        result = await get_recommendations_button(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/companion")
async def ai_companion(
    request: AIRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get AI companion response."""
    try:
        result = await get_companion(db, request.prompt, user_id=current_user.id)
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid AI response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/companion")
async def ai_companion_get_history(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    try:
        result = await get_companion_history(db, user_id=current_user.id)
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail=ai_response_is_not_valid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
