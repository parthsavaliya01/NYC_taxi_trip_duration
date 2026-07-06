"""
NYC Taxi Trip Duration Prediction - FastAPI Backend

Main application entry point with API setup and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.api.predict import router as predict_router
from app.api.analytics import router as analytics_router
from app.db import init_db
from app.core.config import settings
from app.core.logger import setup_logging

logger = setup_logging(__name__)

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="NYC Taxi Trip Duration Prediction API",
    description="RESTful API for predicting NYC taxi trip duration",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        dict: Service status.
    """
    return {"status": "healthy", "environment": settings.environment}


# Root endpoint
@app.get("/", tags=["root"])
async def root() -> dict:
    """
    Root endpoint with API information.
    
    Returns:
        dict: API information.
    """
    return {
        "title": "NYC Taxi Trip Duration Prediction API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc",
        "openapi": "/api/openapi.json"
    }


# Include routers
app.include_router(predict_router)
app.include_router(analytics_router)


# Global exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.
    
    Args:
        request: FastAPI request object.
        exc: Exception instance.
        
    Returns:
        JSONResponse: Error response.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Startup event
@app.on_event("startup")
async def startup():
    """Initialize on application startup."""
    logger.info(f"Starting NYC Taxi API in {settings.environment} environment")
    logger.info(f"API listening on {settings.api.host}:{settings.api.port}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown():
    """Cleanup on application shutdown."""
    logger.info("Shutting down NYC Taxi API")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.api.host,
        port=settings.api.port,
        debug=settings.api.debug,
        reload=settings.api.reload,
        workers=settings.api.workers if not settings.api.debug else 1,
        log_level=settings.logging.level.lower(),
    )