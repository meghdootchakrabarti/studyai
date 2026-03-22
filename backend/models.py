from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from db import Base

class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Demographics
    name = Column(String, nullable=False)
    grade = Column(String, nullable=False)  # e.g., "Class 6"
    board = Column(String, nullable=False)  # e.g., "CBSE", "ICSE"

    # Academic & Interest Data (Stored as JSON for flexibility)
    # Maps to 'dialValues' / 'subjectScores' from frontend: {"Math": 2, "Science": 5, ...}
    subject_scores = Column(JSON, default=dict)
    
    # Maps to 'hobbies' array from frontend: ["Cricket", "Gaming", "Space"]
    hobbies = Column(JSON, default=list)

    # Learning Preferences
    # Maps to 'learnStyle' (e.g., '👀 Reading & Seeing', 'visual')
    learning_style = Column(String, nullable=True)
    
    # Maps to 'depend' (e.g., '🤝 A Good Helper', 'main')
    dependency_level = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<LearnerProfile(name='{self.name}', grade='{self.grade}')>"