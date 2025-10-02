"""
FastAPI dependencies shared across routes.
"""

from typing import Generator
from ..db.session import SessionLocal


def get_db() -> Generator:
    """
    Yields a database session and ensures closing after request lifecycle.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
