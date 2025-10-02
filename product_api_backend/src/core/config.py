"""
Application configuration utilities.

Loads environment variables and provides configuration objects for the app,
including database connection URL.

Do not hard-code secrets; use environment variables configured by orchestrator.
"""

from functools import lru_cache
from pydantic import BaseModel, Field
import os


class AppMeta(BaseModel):
    """Application metadata for OpenAPI and docs styling context."""
    title: str = Field(default="Product Management API", description="API Title")
    description: str = Field(
        default=(
            "Modern, minimal REST API to manage products with fields: id, name, price, quantity.\n\n"
            "Style: Ocean Professional — Blue & amber accents, clean and minimal."
        ),
        description="API Description",
    )
    version: str = Field(default="1.0.0", description="API Version")


class Settings(BaseModel):
    """
    Global application settings.
    Database URL is sourced from environment variables provided by the products_database dependency.
    """
    # IMPORTANT: These env var names are provided by the dependency container; do not guess values.
    # The orchestrator will populate the .env for runtime.
    database_url: str = Field(
        default_factory=lambda: os.getenv("PRODUCTS_DB_URL", ""),
        description="SQLAlchemy Database URL for products_database (e.g., postgresql+psycopg://...)",
    )
    # CORS
    allow_origins: list[str] = Field(default_factory=lambda: ["*"])
    allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    allow_headers: list[str] = Field(default_factory=lambda: ["*"])
    allow_credentials: bool = Field(default=True)

    meta: AppMeta = Field(default_factory=AppMeta)


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
