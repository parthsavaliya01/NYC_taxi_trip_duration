from fastapi import FastAPI
from app.api.predict import router as predict_router
from app.api.analytics import router as analytics_router
from app.db import init_db

app = FastAPI(title="NYC Taxi Duration API")

# Initialize DB
init_db()

app.include_router(predict_router)
app.include_router(analytics_router)

@app.get("/")
def home():
    return {"message": "API is running"}