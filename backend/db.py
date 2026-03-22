import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from your .env file
load_dotenv()

# Define the database URL. 
# Defaults to a local SQLite file (studyai.db) if DATABASE_URL is not found in .env.
# For production/global deployment, add your Postgres URL to .env:
# DATABASE_URL=postgresql://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./studyai.db")

# SQLite requires a special flag to prevent thread sharing issues in FastAPI.
# We apply this conditionally so it doesn't break a future Postgres connection.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Initialize the database engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create a configured "Session" class for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that your SQLAlchemy models (in models.py) will inherit from
Base = declarative_base()

# FastAPI Dependency block
# This function will be injected into your routes to provide a fresh database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()