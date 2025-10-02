from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..core.config import get_settings
from ..db.session import Base, engine
from .routes.products import router as products_router

settings = get_settings()

openapi_tags = [
    {
        "name": "Health",
        "description": "Service health and diagnostics.",
    },
    {
        "name": "Products",
        "description": "CRUD operations for product management.",
    },
]

app = FastAPI(
    title=settings.meta.title,
    description=settings.meta.description,
    version=settings.meta.version,
    openapi_tags=openapi_tags,
    contact={"name": "API Support", "url": "https://example.com/support"},
    license_info={"name": "MIT License"},
)

# Apply CORS with settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

# Create database tables at startup (simple auto-migrate)
@app.on_event("startup")
def on_startup():
    """
    Ensure database tables exist.
    """
    Base.metadata.create_all(bind=engine)

# Register Routers
app.include_router(products_router)


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Returns service health status.",
)
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}
