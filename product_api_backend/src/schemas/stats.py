"""
Pydantic schemas for aggregate/statistics responses.
"""

from pydantic import BaseModel, Field


class TotalBalanceOut(BaseModel):
    """
    Total balance/value of all products in stock.
    """
    total: float = Field(..., description="Sum of price * quantity across all products")

    class Config:
        from_attributes = True
