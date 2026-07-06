"""
Setup configuration for NYC Taxi Trip Duration Prediction.

Enables installation via pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nyc-taxi-prediction",
    version="1.0.0",
    author="Parth",
    author_email="your.email@example.com",
    description="End-to-end ML project predicting NYC taxi trip duration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nyc-taxi-prediction",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Web Framework
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "pydantic==2.4.2",
        "pydantic-settings==2.0.3",
        
        # Streamlit Frontend
        "streamlit==1.28.1",
        
        # Machine Learning & Data Processing
        "scikit-learn==1.3.2",
        "pandas==2.1.1",
        "numpy==1.26.2",
        "lightgbm==4.1.1",
        "xgboost==2.0.2",
        "joblib==1.3.2",
        
        # Geospatial
        "h3==3.7.10",
        
        # HTTP & APIs
        "requests==2.31.0",
        "aiohttp==3.9.1",
        
        # Utilities
        "python-dotenv==1.0.0",
        "python-multipart==0.0.6",
        
        # Logging & Monitoring
        "python-json-logger==2.0.7",
        # Hugging Face Hub for model artifact downloads
        "huggingface_hub==0.20.1",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
            "black==23.11.0",
            "flake8==6.1.0",
            "mypy==1.7.1",
            "pre-commit==3.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nyc-taxi-api=app.main:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
