import streamlit as st
import requests
from datetime import datetime
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NYC Taxi App", layout="centered")

st.title("🚖 NYC Taxi Duration Predictor")

# -----------------------------
# INPUT FORM
# -----------------------------
st.subheader("📍 Enter Trip Details")

col1, col2 = st.columns(2)

with col1:
    vendor_id = st.selectbox("Vendor ID", [1, 2])
    passenger_count = st.slider("Passenger Count", 1, 6, 1)
    pickup_lat = st.number_input("Pickup Latitude", value=40.75)
    pickup_lon = st.number_input("Pickup Longitude", value=-73.99)

with col2:
    store_flag = st.selectbox("Store & Forward Flag", ["N", "Y"])
    dropoff_lat = st.number_input("Dropoff Latitude", value=40.76)
    dropoff_lon = st.number_input("Dropoff Longitude", value=-73.98)
    pickup_datetime = st.datetime_input("Pickup Time", datetime.now())

# -----------------------------
# PREDICT
# -----------------------------
if st.button("🚀 Predict Duration", use_container_width=True):

    payload = {
        "vendor_id": vendor_id,
        "passenger_count": passenger_count,
        "pickup_latitude": pickup_lat,
        "pickup_longitude": pickup_lon,
        "dropoff_latitude": dropoff_lat,
        "dropoff_longitude": dropoff_lon,
        "pickup_datetime": str(pickup_datetime),
        "store_and_fwd_flag": store_flag
    }

    try:
        response = requests.post(f"{API_URL}/predict", json=payload)

        if response.status_code == 200:
            result = response.json()

            duration_sec = result["trip_duration"]
            duration_min = duration_sec / 60

            st.success("✅ Prediction Successful")

            st.metric("⏱ Duration (min)", f"{duration_min:.2f}")
            st.caption(f"{duration_sec:.0f} seconds")

        else:
            st.error("❌ API Error")

    except Exception as e:
        st.error(f"⚠️ Connection Error: {e}")

# -----------------------------
# ANALYTICS DASHBOARD
# -----------------------------
st.divider()
st.subheader("📊 Analytics Dashboard")

if st.button("Load Analytics"):

    try:
        res = requests.get(f"{API_URL}/analytics")

        if res.status_code == 200:
            data = res.json()

            st.metric("Total Predictions", data["total_predictions"])
            st.metric("Avg Duration (sec)", f"{data['avg_duration']:.2f}")

            df = pd.DataFrame(data["daily"], columns=["date", "count"])
            df["date"] = pd.to_datetime(df["date"])

            st.line_chart(df.set_index("date"))

        else:
            st.error("❌ Failed to load analytics")

    except Exception as e:
        st.error(f"⚠️ API Connection Error: {e}")