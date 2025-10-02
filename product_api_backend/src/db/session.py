"""
Database session and engine initialization using SQLAlchemy.
The database URL is sourced from environment variables via core.config.get_settings().
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import get_settings

settings = get_settings()

if not settings.database_url:
    # Provide a safe fallback for local dev if env isn't set (SQLite file).
    # For production, orchestrator should set PRODUCTS_DB_URL for products_database.
    database_url = "sqlite:///./products.db"
else:
    database_url = settings.database_url

# For SQLite, need check_same_thread; SQLAlchemy auto-handles most dialects.
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

engine = create_engine(database_url, echo=False, future=True, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()
