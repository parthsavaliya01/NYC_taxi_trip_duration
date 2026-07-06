# NYC Taxi Trip Duration Prediction

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-style machine learning project that predicts New York City taxi trip duration using a trained LightGBM-based regression pipeline, a FastAPI backend, and an interactive Streamlit interface.

## 1. Project Overview

This project solves the problem of estimating taxi trip duration from trip attributes such as pickup and dropoff location, passenger count, vendor information, and pickup time. The goal is to provide a fast and practical prediction tool for ride-hailing and fleet operations, where accurate travel-time estimates improve planning, dispatching, and customer communication.

The project is designed for developers, data scientists, and recruiters who want to see an end-to-end ML application that includes data preprocessing, model inference, API development, a web UI, and deployment-ready configuration.

## 2. Features

- End-to-end taxi trip duration prediction
- Interactive Streamlit web application
- REST API built with FastAPI
- Analytics endpoint for stored predictions
- SQLite-based prediction history storage
- Feature engineering for geospatial and temporal inputs
- Docker support for local deployment
- Environment-based configuration

## 3. Technology Stack

### Frontend
- Streamlit

### Backend
- FastAPI
- Uvicorn

### Programming Language
- Python 3.8+

### Database
- SQLite

### Machine Learning
- Scikit-learn
- LightGBM
- Joblib
- NumPy
- Pandas

### Deployment
- Docker
- Docker Compose
- Nginx configuration included

## 4. AI / ML Model Information

The application loads a trained regression pipeline automatically from Hugging Face Hub. The model is stored in the remote repository `parthsavaliya001/nyc-taxi-trip-duration-model` and downloaded using the `huggingface_hub` cache.

Why this model was selected:
- Strong performance on tabular data
- Fast training and inference
- Well-suited to nonlinear relationships in travel-time prediction

Model pipeline details:
- Feature engineering is handled by custom transformers in app/features/custom_transformers.py
- The trained pipeline is downloaded and loaded through app/model/model_loader.py
- Inference is performed through the prediction service in app/services/predictor.py

Model evaluation:
- The repository includes a trained model artifact and completed notebook workflow
- Published evaluation metrics are not included in this snapshot, so the project is documented as a functional inference pipeline rather than a benchmark report

## 5. Project Workflow

User Input

↓

Trip Feature Collection

↓

Feature Engineering and Preprocessing

↓

Model Inference

↓

Prediction Output

↓

Database Storage

↓

Analytics and UI Display

In this project, the user enters trip information in the Streamlit interface or through the API. The backend transforms the request into engineered features, uses the trained model to estimate trip duration, stores the result in SQLite, and returns the output for display in the UI or API response.

## 6. Project Architecture

The application follows a simple three-layer structure:

- Frontend: Streamlit provides the interactive prediction and analytics experience
- Backend: FastAPI exposes prediction and analytics endpoints
- Model Layer: A trained scikit-learn pipeline loads the LightGBM model for inference
- Data Layer: SQLite stores prediction records for later analysis

Communication flow:
1. The user submits trip details through the frontend or API
2. FastAPI routes the request to the prediction service
3. The prediction service loads the trained pipeline and returns a duration estimate
4. The result is saved to the local database and returned to the user

## 7. Folder Structure

```text
nyc_taxi_app/
├── app/
│   ├── api/
│   ├── core/
│   ├── features/
│   ├── model/
│   ├── schema/
│   ├── services/
│   └── db.py
├── streamlit_app/
├── data/
├── logs/
├── nginx/
├── Dockerfile
├── Dockerfile.streamlit
├── docker-compose.yml
├── requirements.txt
├── setup.py
├── start_backend.sh
├── start_frontend.sh
├── .env.example
└── README.md
```

Key folders:
- app/: backend application, API routes, services, model loading, and database interactions
- streamlit_app/: interactive Streamlit frontend
- data/: model artifacts and runtime data storage
- logs/: application log output
- nginx/: reverse proxy configuration

## 8. Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd nyc_taxi_app
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

The trained model pipeline is downloaded automatically from Hugging Face Hub when the application starts. No local model artifact is required in the repository.

## 9. How to Run the Project

### Option 1: Run the backend

```bash
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Run the frontend

```bash
source venv/bin/activate
streamlit run streamlit_app/app.py
```

### Option 3: Use the provided scripts

```bash
./start_backend.sh
./start_frontend.sh
```

### Option 4: Run with Docker Compose

```bash
docker compose up --build
```

Access points:
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/api/docs
- Streamlit UI: http://localhost:8501

## 10. Environment Variables

Copy .env.example to .env and adjust the values as needed.

| Variable | Purpose | Example |
|---|---|---|
| ENVIRONMENT | Application environment | development |
| DEBUG | Enable debug mode | False |
| API_HOST | FastAPI host binding | 0.0.0.0 |
| API_PORT | FastAPI port | 8000 |
| API_DEBUG | FastAPI debug flag | False |
| API_RELOAD | Enable auto-reload | False |
| API_WORKERS | Number of API workers | 4 |
| STREAMLIT_API_URL | Backend URL used by Streamlit | http://localhost:8000 |
| STREAMLIT_TIMEOUT | Request timeout for frontend calls | 30 |
| DB_PATH | SQLite database path | data/artifacts/predictions.db |
| DB_POOL_SIZE | Database pool size | 5 |
| DB_TIMEOUT | Database timeout in seconds | 5.0 |
| MODEL_REPO | Hugging Face model repository | parthsavaliya001/nyc-taxi-trip-duration-model |
| MODEL_FILENAME | Model file name in the repo | taxi_full_pipeline.pkl |
| MODEL_VERSION | Model version label | 1.0.0 |
| LOG_LEVEL | Logging level | INFO |
| LOG_FILE | Log file destination | logs/app.log |
| N_CLUSTERS | Number of clustering centers | 30 |
| RANDOM_STATE | Random seed | 42 |


## 11. Future Improvements

Potential next steps for this project:
- Add model performance monitoring and drift detection
- Expand analytics with richer charts and filtering
- Add authentication and user accounts
- Improve deployment with CI/CD automation
- Package the model and app as a more production-focused service

## 12. License

This project is licensed under the MIT License. See LICENSE for details.

## 13. Author

Built as a portfolio-ready machine learning application by Parth.

GitHub: https://github.com/parthsavaliya01
