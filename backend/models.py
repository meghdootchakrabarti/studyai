from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from db import Base

class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    grade = Column(String, nullable=False)  # e.g., "Class 6"
    board = Column(String, nullable=False)  # e.g., "CBSE", "ICSE"

    subject_scores = Column(JSON, default=dict)

    hobbies = Column(JSON, default=list)

    learning_style = Column(String, nullable=True)

    dependency_level = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<LearnerProfile(name='{self.name}', grade='{self.grade}')>"
