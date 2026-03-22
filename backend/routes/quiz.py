from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Optional
from ai import ask_ai

router = APIRouter(prefix="/api/quiz", tags=["quiz"])


class QuizRequest(BaseModel):
    subject: Optional[str] = ""
    profile: Optional[Dict[str, Any]] = {}


@router.get("")
async def quiz_info():
    return {"message": "Send a POST request with subject and profile to generate a quiz."}


@router.post("")
async def generate_quiz(req: QuizRequest):
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

    subject_hint = f" Focus on {req.subject}." if req.subject else ""
    prompt = (
        f"Give me a quick 3-question quiz appropriate for my grade level and curriculum.{subject_hint} "
        "Format each question clearly with the question number, the question text, and 4 multiple choice options (A, B, C, D). "
        "Do not reveal the answers yet."
    )

    reply = await ask_ai(prompt, [], normalized_profile)
    return {"quiz": reply}
