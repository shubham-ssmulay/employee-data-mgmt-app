"""
Database configuration and session utilities.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
from models.employee import Base


DB_URL = os.getenv("DATABASE_URL", "sqlite:///./employees.db")


engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_db_and_tables():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database setup complete.")


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()