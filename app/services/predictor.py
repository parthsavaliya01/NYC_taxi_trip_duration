import pandas as pd
import numpy as np
from app.model.load_model import pipeline
from app.db import insert_prediction

def predict(data):
    try:
        df = pd.DataFrame([data])

        prediction = pipeline.predict(df)

        # Convert from log scale
        duration = np.expm1(prediction[0])

        # simple distance
        distance = abs(data["pickup_latitude"] - data["dropoff_latitude"]) + \
                   abs(data["pickup_longitude"] - data["dropoff_longitude"])

        # Save to DB
        try:
            insert_prediction(data, duration, distance)
        except Exception as e:
            print("DB Error:", e)

        return float(duration)

    except Exception as e:
        print("Prediction Error:", e)
        raise e