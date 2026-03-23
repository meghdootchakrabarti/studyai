from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import engine, Base
import models  # This ensures the LearnerProfile model is registered before creating tables

from routes import chat, profile
from routes import quiz  # Uncommented

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StudyAI API",
    description="Backend for the AI Study Companion",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins during development. (Change this for production!)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(profile.router)
app.include_router(chat.router)
app.include_router(quiz.router)

@app.get("/")
def read_root():
    """
    A simple endpoint to verify the server is up and running.
    """
    return {
        "status": "online",
        "message": "Welcome to the StudyAI Backend! 🚀",
        "endpoints": ["/api/profile", "/api/chat", "/docs"]
    }
