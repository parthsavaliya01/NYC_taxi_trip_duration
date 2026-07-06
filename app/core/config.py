"""
Configuration management for NYC Taxi Trip Duration Prediction.

Loads configuration from environment variables with sensible defaults.
Supports multiple environments: development, staging, production.
"""

import os
from typing import Optional
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass
class DatabaseConfig:
    """Database configuration."""
    path: str = os.getenv("DB_PATH", "data/artifacts/predictions.db")
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    timeout: float = float(os.getenv("DB_TIMEOUT", "5.0"))
    
    def __post_init__(self) -> None:
        """Ensure database directory exists."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)


@dataclass
class APIConfig:
    """API configuration."""
    host: str = os.getenv("API_HOST", "0.0.0.0")
    port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("API_DEBUG", "False").lower() == "true"
    reload: bool = os.getenv("API_RELOAD", "False").lower() == "true"
    workers: int = int(os.getenv("API_WORKERS", "4"))


@dataclass
class StreamlitConfig:
    """Streamlit configuration."""
    api_url: str = os.getenv("STREAMLIT_API_URL", "http://localhost:8000")
    page_title: str = "NYC Taxi Duration Predictor"
    layout: str = "centered"
    request_timeout: int = int(os.getenv("STREAMLIT_TIMEOUT", "30"))


@dataclass
class ModelConfig:
    """Model configuration."""
    model_repo: str = os.getenv(
        "MODEL_REPO", "parthsavaliya001/nyc-taxi-trip-duration-model"
    )
    model_filename: str = os.getenv("MODEL_FILENAME", "taxi_full_pipeline.pkl")
    version: str = os.getenv("MODEL_VERSION", "1.0.0")


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = os.getenv("LOG_FILE", "logs/app.log")
    
    def __post_init__(self) -> None:
        """Ensure logs directory exists."""
        if self.log_file:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)


@dataclass
class Settings:
    """Main application settings."""
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    api: APIConfig = field(default_factory=APIConfig)
    streamlit: StreamlitConfig = field(default_factory=StreamlitConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Feature engineering
    n_clusters: int = int(os.getenv("N_CLUSTERS", "30"))
    random_state: int = int(os.getenv("RANDOM_STATE", "42"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get settings instance (cached).
    
    Returns:
        Settings: Application settings instance.
    """
    return Settings()


# For immediate access
settings = get_settings()
