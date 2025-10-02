"""
Pydantic schemas for Product resource.
"""

from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    """
    Base properties shared across create and update.
    """
    name: str = Field(..., description="Name of the product", min_length=1, max_length=255)
    price: float = Field(..., description="Unit price of the product", ge=0)
    quantity: int = Field(..., description="Available quantity in stock", ge=0)

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        # Keep two decimal precision in representation (stored as float in DB).
        return float(round(v, 2))


class ProductCreate(ProductBase):
    """
    Schema for creating a product.
    """
    pass


class ProductUpdate(ProductBase):
    """
    Schema for updating a product.
    """
    pass


class ProductOut(ProductBase):
    """
    Response schema for a product including ID.
    """
    id: int = Field(..., description="Unique identifier of the product")

    class Config:
        from_attributes = True
