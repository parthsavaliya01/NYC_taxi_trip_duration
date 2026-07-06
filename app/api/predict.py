"""
API endpoints for taxi trip duration prediction.

Provides REST API for making predictions and retrieving results.
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import logging

from app.schema.predict_schema import TaxiInput, PredictionResponse, ErrorResponse
from app.services.predictor import predict_and_save
from app.core.logger import setup_logging

logger = setup_logging(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["predictions"],
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict taxi trip duration",
    description="Predict the duration of a taxi trip based on trip details"
)
def get_prediction(input_data: TaxiInput) -> PredictionResponse:
    """
    Predict taxi trip duration.
    
    Accepts trip information and returns predicted duration in seconds and minutes.
    
    Args:
        input_data: Trip information (validated by TaxiInput schema).
        
    Returns:
        PredictionResponse: Predicted trip duration.
        
    Raises:
        HTTPException: If prediction fails.
        
    Example:
        ```json
        POST /api/v1/predict
        {
            "vendor_id": 1,
            "passenger_count": 2,
            "pickup_latitude": 40.75,
            "pickup_longitude": -73.99,
            "dropoff_latitude": 40.76,
            "dropoff_longitude": -73.98,
            "pickup_datetime": "2024-06-21T14:30:00",
            "store_and_fwd_flag": "N"
        }
        ```
    """
    try:
        # Convert input to dict for prediction service
        data = input_data.dict()
        data["pickup_datetime"] = input_data.pickup_datetime.isoformat()
        
        # Make prediction
        duration_seconds = predict_and_save(data)
        duration_minutes = duration_seconds / 60
        
        logger.info(f"Prediction successful: {duration_seconds:.2f}s")
        
        return PredictionResponse(
            trip_duration=round(duration_seconds, 2),
            trip_duration_minutes=round(duration_minutes, 2)
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction failed. Please try again later.",
        )