from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import get_response
from typing import Optional, List, Dict, Any

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_profile: Optional[Dict[str, Any]] = None

@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    reply = get_response(req.message, user_profile=req.user_profile)
    return {"reply": reply}
