from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import database engine and Base to initialize tables
from db import engine, Base
import models  # This ensures the LearnerProfile model is registered before creating tables

# Import your route handlers
from routes import chat, profile
from routes import quiz  # Uncommented

# ─── DATABASE INITIALIZATION ─────────────────────────────────────────────────
# This command automatically creates 'studyai.db' and the 'learner_profiles' 
# table the first time you run the app. 
Base.metadata.create_all(bind=engine)

# ─── APP INITIALIZATION ──────────────────────────────────────────────────────
app = FastAPI(
    title="StudyAI API",
    description="Backend for the AI Study Companion",
    version="1.0.0"
)

# ─── CORS CONFIGURATION ──────────────────────────────────────────────────────
# CRITICAL: Since your frontend (HTML/JS) and backend (FastAPI) might run on 
# different ports (e.g., frontend on 5500, backend on 8000) or as local files,
# CORS allows the browser to make requests to the API without blocking them.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins during development. (Change this for production!)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# ─── ROUTER REGISTRATION ─────────────────────────────────────────────────────
# This "plugs in" the endpoints we built in the 'routes' folder
app.include_router(profile.router)
app.include_router(chat.router)
app.include_router(quiz.router)

# ─── HEALTH CHECK ────────────────────────────────────────────────────────────
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