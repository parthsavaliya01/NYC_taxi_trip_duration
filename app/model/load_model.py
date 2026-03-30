import joblib

from app.features.custom_transformers import (
    EnhancedNYCFeatureEngineer,
    ColumnSelector,
    LogTransformer
)

pipeline = joblib.load("app/model/taxi_full_pipeline.pkl")
