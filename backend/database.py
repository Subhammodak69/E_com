from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import credentials
import time

# Database URL
URL_DATABASE = credentials.DATABASE_CREDENTIALS

# Engine and session setup
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency function with debug logs and timing
def get_db() -> Generator[Session, None, None]:
    print("Opening new DB session...")
    start = time.perf_counter()
    db = SessionLocal()
    duration = time.perf_counter() - start
    print(f"DB session opened in {duration:.4f} seconds")
    try:
        yield db
    finally:
        db.close()
        print("DB session closed.")
