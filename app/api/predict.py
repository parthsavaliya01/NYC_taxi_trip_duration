from fastapi import APIRouter
from app.schema.predict_schema import TaxiInput
from app.services.predictor import predict

router = APIRouter()

@router.post("/predict")
def get_prediction(input_data: TaxiInput):
    result = predict(input_data.dict())
    return {"trip_duration": result}