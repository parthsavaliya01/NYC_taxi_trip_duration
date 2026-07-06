"""
Pydantic schemas for API request/response validation.

Provides type-safe request/response models with validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class VendorIDEnum(str, Enum):
    """Taxi vendor IDs."""
    VENDOR_1 = 1
    VENDOR_2 = 2


class StoreForwardFlagEnum(str, Enum):
    """Store and forward flags."""
    NO = "N"
    YES = "Y"


class TaxiInput(BaseModel):
    """
    Input schema for taxi trip prediction.
    
    All fields are validated for reasonable ranges and types.
    """
    
    vendor_id: int = Field(
        ...,
        ge=1,
        le=2,
        description="Taxi vendor ID (1 or 2)"
    )
    
    passenger_count: int = Field(
        ...,
        ge=1,
        le=6,
        description="Number of passengers (1-6)"
    )
    
    pickup_latitude: float = Field(
        ...,
        ge=40.5,
        le=40.95,
        description="Pickup location latitude (NYC bounds)"
    )
    
    pickup_longitude: float = Field(
        ...,
        ge=-74.3,
        le=-73.7,
        description="Pickup location longitude (NYC bounds)"
    )
    
    dropoff_latitude: float = Field(
        ...,
        ge=40.5,
        le=40.95,
        description="Dropoff location latitude (NYC bounds)"
    )
    
    dropoff_longitude: float = Field(
        ...,
        ge=-74.3,
        le=-73.7,
        description="Dropoff location longitude (NYC bounds)"
    )
    
    pickup_datetime: datetime = Field(
        ...,
        description="Pickup datetime in ISO format"
    )
    
    store_and_fwd_flag: str = Field(
        default="N",
        pattern="^[NY]$",
        description="Store and forward flag (Y/N)"
    )
    
    @field_validator('pickup_datetime')
    @classmethod
    def validate_pickup_datetime(cls, v: datetime) -> datetime:
        """Validate pickup datetime is not in future."""
        if v > datetime.now():
            raise ValueError("Pickup datetime cannot be in the future")
        return v
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "vendor_id": 1,
                "passenger_count": 2,
                "pickup_latitude": 40.75,
                "pickup_longitude": -73.99,
                "dropoff_latitude": 40.76,
                "dropoff_longitude": -73.98,
                "pickup_datetime": "2024-06-21T14:30:00",
                "store_and_fwd_flag": "N"
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for prediction endpoint."""
    
    trip_duration: float = Field(
        ...,
        ge=0,
        description="Predicted trip duration in seconds"
    )
    
    trip_duration_minutes: float = Field(
        ...,
        ge=0,
        description="Predicted trip duration in minutes"
    )
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "trip_duration": 720.5,
                "trip_duration_minutes": 12.01
            }
        }


class AnalyticsStats(BaseModel):
    """Statistics for analytics endpoint."""
    
    total_predictions: int = Field(
        ...,
        ge=0,
        description="Total number of predictions made"
    )
    
    avg_duration: float = Field(
        ...,
        ge=0,
        description="Average prediction duration in seconds"
    )
    
    min_duration: float = Field(
        ...,
        ge=0,
        description="Minimum prediction duration in seconds"
    )
    
    max_duration: float = Field(
        ...,
        ge=0,
        description="Maximum prediction duration in seconds"
    )
    
    stddev_duration: float = Field(
        ...,
        ge=0,
        description="Standard deviation of prediction duration"
    )
    
    daily: list = Field(
        default_factory=list,
        description="Daily statistics"
    )


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    detail: str = Field(
        ...,
        description="Error message"
    )
    
    error_code: Optional[str] = Field(
        default=None,
        description="Error code for programmatic handling"
    )
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "detail": "Invalid input data",
                "error_code": "INVALID_INPUT"
            }
        }