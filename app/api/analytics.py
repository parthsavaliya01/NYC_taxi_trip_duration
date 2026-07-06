"""
API endpoints for analytics and statistics.

Provides endpoints for retrieving prediction statistics and analytics.
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import logging

from app.db import get_stats
from app.schema.predict_schema import AnalyticsStats, ErrorResponse
from app.core.logger import setup_logging

logger = setup_logging(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["analytics"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)


@router.get(
    "/analytics",
    response_model=AnalyticsStats,
    summary="Get prediction analytics",
    description="Retrieve statistics about all predictions made by the system"
)
def analytics() -> AnalyticsStats:
    """
    Get prediction statistics and analytics.
    
    Returns aggregated statistics across all predictions including:
    - Total number of predictions
    - Average, min, max, and standard deviation of durations
    - Daily statistics for the last 30 days
    
    Returns:
        AnalyticsStats: Analytics data.
        
    Raises:
        HTTPException: If statistics retrieval fails.
        
    Example:
        ```json
        GET /api/v1/analytics
        
        Response:
        {
            "total_predictions": 42,
            "avg_duration": 720.5,
            "min_duration": 120.0,
            "max_duration": 3600.0,
            "stddev_duration": 450.2,
            "daily": [...]
        }
        ```
    """
    try:
        stats = get_stats()
        logger.info(f"Analytics retrieved: {stats['total_predictions']} predictions")
        return AnalyticsStats(**stats)
        
    except Exception as e:
        logger.error(f"Failed to retrieve analytics: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analytics. Please try again later.",
        )