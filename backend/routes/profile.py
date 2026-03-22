from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, List
from db import get_db
from models import LearnerProfile

router = APIRouter(prefix="/api/profile", tags=["profile"])


class ProfileCreate(BaseModel):
    name: str
    classValue: str
    board: str
    school: Optional[str] = ""
    dialValues: Optional[Dict[str, int]] = {}
    hobbies: Optional[List[str]] = []
    customHobby: Optional[str] = ""
    learnStyle: Optional[str] = ""
    depend: Optional[str] = ""


@router.post("")
def create_profile(data: ProfileCreate, db: Session = Depends(get_db)):
    all_hobbies = data.hobbies or []
    if data.customHobby:
        all_hobbies = all_hobbies + [data.customHobby]

    profile = LearnerProfile(
        name=data.name,
        grade=data.classValue,
        board=data.board,
        subject_scores=data.dialValues,
        hobbies=all_hobbies,
        learning_style=data.learnStyle,
        dependency_level=data.depend,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return {"id": profile.id, "message": "Profile saved!"}


@router.get("/{profile_id}")
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(LearnerProfile).filter(LearnerProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "id": profile.id,
        "name": profile.name,
        "grade": profile.grade,
        "board": profile.board,
        "subject_scores": profile.subject_scores,
        "hobbies": profile.hobbies,
        "learning_style": profile.learning_style,
        "dependency_level": profile.dependency_level,
        "created_at": profile.created_at,
    }
