from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from app.routes import analysis
from app.utils.logger import setup_logging, LoggingMiddleware
import logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Veefyed Skin Analysis API",
    description="""
    Backend service for the Veefyed mobile application.
    
    This API provides endpoints for secure image processing and mock skin analysis. It is designed with a focus on clean architecture, security, and maintainability.

    Key Features:
    - Image Upload: Validated file upload handling with secure storage.
    - Analysis Engine: Mock implementation of AI-driven skin analysis logic.
    - Security: API Key authentication layer for all protected endpoints.

    Authentication:
    All API endpoints require valid authentication credentials.
    
    Header Parameter: X-API-Key
    Default Value: secret-token-123
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

app.include_router(analysis.router, tags=["Analysis"])


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js"
    )


@app.get("/", tags=["General"])
def root():
    return {
        "service": "Image Analysis API",
        "status": "running",
        "documentation": "/docs",
        "redoc": "/redoc"
    }