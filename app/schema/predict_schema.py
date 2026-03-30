from pydantic import BaseModel

class TaxiInput(BaseModel):
    vendor_id: int   # 🔥 ADD THIS
    passenger_count: int
    pickup_latitude: float
    pickup_longitude: float
    dropoff_latitude: float
    dropoff_longitude: float
    pickup_datetime: str
    store_and_fwd_flag: str = "N"   # optional but safer