from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ai import ask_ai

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    user_message: str
    chat_history: Optional[List[ChatMessage]] = []
    profile: Optional[Dict[str, Any]] = {}


@router.post("")
async def chat(req: ChatRequest):
    history = [{"role": m.role, "content": m.content} for m in req.chat_history]

    profile = req.profile or {}
    normalized_profile = {
        "name": profile.get("name", "Student"),
        "grade": profile.get("classValue") or profile.get("grade", ""),
        "board": profile.get("board", ""),
        "subject_scores": profile.get("dialValues") or profile.get("subject_scores", {}),
        "hobbies": profile.get("hobbies", []),
        "learning_style": profile.get("learnStyle") or profile.get("learning_style", ""),
        "dependency_level": profile.get("depend") or profile.get("dependency_level", ""),
    }

    reply = await ask_ai(req.user_message, history, normalized_profile)
    return {"reply": reply}
