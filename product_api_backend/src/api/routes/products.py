"""
Product routes: RESTful CRUD endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from ...schemas.product import ProductOut, ProductCreate, ProductUpdate
from ...schemas.stats import TotalBalanceOut
from ...crud import product as crud_product
from ..deps import get_db

router = APIRouter(prefix="/products", tags=["Products"])


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[ProductOut],
    summary="List products",
    description="Retrieve a paginated list of products.",
    responses={
        200: {"description": "List of products retrieved successfully"},
    },
)
def list_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of records to return"),
    db: Session = Depends(get_db),
) -> List[ProductOut]:
    """List products with pagination."""
    return crud_product.get_multi(db, skip=skip, limit=limit)


# PUBLIC_INTERFACE
@router.get(
    "/{product_id}",
    response_model=ProductOut,
    summary="Get product",
    description="Retrieve a single product by its ID.",
    responses={
        200: {"description": "Product retrieved successfully"},
        404: {"description": "Product not found"},
    },
)
def get_product(
    product_id: int = Path(..., ge=1, description="ID of the product"),
    db: Session = Depends(get_db),
) -> ProductOut:
    """Get a product by ID."""
    obj = crud_product.get(db, product_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return obj


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description="Create a new product.",
    responses={
        201: {"description": "Product created successfully"},
        422: {"description": "Validation error"},
    },
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductOut:
    """Create a product."""
    return crud_product.create(db, payload)


# PUBLIC_INTERFACE
@router.put(
    "/{product_id}",
    response_model=ProductOut,
    summary="Update product",
    description="Update an existing product by ID.",
    responses={
        200: {"description": "Product updated successfully"},
        404: {"description": "Product not found"},
        422: {"description": "Validation error"},
    },
)
def update_product(
    product_id: int = Path(..., ge=1, description="ID of the product"),
    payload: ProductUpdate = ...,
    db: Session = Depends(get_db),
) -> ProductOut:
    """Update a product by ID."""
    obj = crud_product.get(db, product_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return crud_product.update(db, obj, payload)


# PUBLIC_INTERFACE
@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Delete a product by ID.",
    responses={
        204: {"description": "Product deleted successfully"},
        404: {"description": "Product not found"},
    },
)
def delete_product(
    product_id: int = Path(..., ge=1, description="ID of the product"),
    db: Session = Depends(get_db),
) -> None:
    """Delete a product by ID."""
    deleted = crud_product.remove(db, product_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return None


# PUBLIC_INTERFACE
@router.get(
    "/total-balance",
    response_model=TotalBalanceOut,
    summary="Get total balance of stock",
    description=(
        "Calculate and return the total monetary value of the stock as the sum of price * quantity "
        "for all products. If there are no products, returns 0."
    ),
    responses={
        200: {"description": "Total balance calculated successfully"},
    },
)
def get_total_balance(
    db: Session = Depends(get_db),
) -> TotalBalanceOut:
    """
    Endpoint to compute total balance of all products in stock.

    Returns:
        TotalBalanceOut: Object containing the numeric total. Edge case: returns 0 when no products exist.
    """
    total = crud_product.total_balance(db)
    return TotalBalanceOut(total=total)
