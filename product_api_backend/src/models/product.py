"""
SQLAlchemy Product model.
"""

from sqlalchemy import Column, Integer, String, Float
from ..db.session import Base


class Product(Base):
    """
    ORM model for the products table.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=255), nullable=False, index=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
