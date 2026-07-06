"""
Prediction service for taxi trip duration.

Handles model predictions with proper error handling and logging.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Tuple
from math import radians, sin, cos, sqrt, atan2

from app.model.model_loader import get_pipeline
from app.db import insert_prediction
from app.core.logger import setup_logging

logger = setup_logging(__name__)


def _calculate_distance(
    pickup_lat: float,
    pickup_lon: float,
    dropoff_lat: float,
    dropoff_lon: float
) -> float:
    """
    Calculate distance using the haversine formula.

    Args:
        pickup_lat: Pickup latitude.
        pickup_lon: Pickup longitude.
        dropoff_lat: Dropoff latitude.
        dropoff_lon: Dropoff longitude.

    Returns:
        float: Distance in kilometers.

    Raises:
        ValueError: If coordinates are invalid.
    """
    try:
        lat1, lon1, lat2, lon2 = map(radians, [pickup_lat, pickup_lon, dropoff_lat, dropoff_lon])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6371.0 * c
        return max(distance, 0.0)
    except Exception as e:
        logger.error(f"Distance calculation error: {e}")
        raise ValueError(f"Failed to calculate distance: {e}")


def predict(data: Dict[str, Any]) -> Tuple[float, float]:
    """
    Predict taxi trip duration from input data.
    
    Args:
        data: Input dictionary with trip information.
        
    Returns:
        Tuple[float, float]: (duration_seconds, distance_km)
        
    Raises:
        ValueError: If prediction fails or invalid data.
        RuntimeError: If model loading fails.
    """
    try:
        # Create DataFrame for pipeline
        df = pd.DataFrame([data])
        
        logger.debug(f"Processing prediction for vendor {data.get('vendor_id')}")
        
        # Load the pipeline from Hugging Face Hub cache and make a prediction.
        pipeline = get_pipeline()
        prediction = pipeline.predict(df)
        
        if prediction is None or len(prediction) == 0:
            raise RuntimeError("Model returned empty prediction")
        
        # Convert from log scale back to original scale
        duration_seconds = float(np.expm1(prediction[0]))
        
        # Validate output
        if duration_seconds <= 0:
            logger.warning(f"Negative/zero duration predicted: {duration_seconds}")
            duration_seconds = max(duration_seconds, 60.0)  # Minimum 1 minute
        
        # Calculate distance consistently with training
        distance = _calculate_distance(
            data["pickup_latitude"],
            data["pickup_longitude"],
            data["dropoff_latitude"],
            data["dropoff_longitude"]
        )
        
        logger.info(
            f"Prediction: duration={duration_seconds:.2f}s, distance={distance:.2f}km"
        )
        
        return duration_seconds, distance
        
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise


def predict_and_save(data: Dict[str, Any]) -> float:
    """
    Make prediction and save to database.
    
    Args:
        data: Input dictionary with trip information.
        
    Returns:
        float: Predicted trip duration in seconds.
        
    Raises:
        ValueError: If prediction fails.
    """
    try:
        duration, distance = predict(data)
        
        # Save to database
        try:
            insert_prediction(data, duration, distance)
            logger.debug("Prediction saved to database")
        except Exception as db_error:
            logger.warning(f"Failed to save prediction to database: {db_error}")
            # Don't fail the prediction if database fails
        
        return duration
        
    except Exception as e:
        logger.error(f"Prediction and save failed: {e}", exc_info=True)
        raise