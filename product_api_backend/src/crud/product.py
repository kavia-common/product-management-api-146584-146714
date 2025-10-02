"""
CRUD operations for Product.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductUpdate


def get(db: Session, product_id: int) -> Optional[Product]:
    """Get a single product by ID."""
    return db.get(Product, product_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    """Get multiple products with pagination."""
    return db.query(Product).offset(skip).limit(limit).all()


def create(db: Session, obj_in: ProductCreate) -> Product:
    """Create a new product."""
    db_obj = Product(name=obj_in.name, price=obj_in.price, quantity=obj_in.quantity)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Product, obj_in: ProductUpdate) -> Product:
    """Update an existing product."""
    db_obj.name = obj_in.name
    db_obj.price = obj_in.price
    db_obj.quantity = obj_in.quantity
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, product_id: int) -> Optional[Product]:
    """Delete a product by ID, returning the deleted object if exists."""
    obj = get(db, product_id)
    if obj is None:
        return None
    db.delete(obj)
    db.commit()
    return obj
