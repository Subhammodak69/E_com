from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import credentials

# Database connection URL
URL_DATABASE = credentials.DATABASE_CREDENTIALS


# Create SQLAlchemy engine
engine = create_engine(URL_DATABASE)


# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for models
Base = declarative_base()


# Dependency function for FastAPI to get a session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
