"""
Streamlit UI for NYC Taxi Trip Duration Prediction.

Interactive web application for making predictions and viewing analytics.
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_URL = os.getenv("STREAMLIT_API_URL", "http://localhost:8000")
REQUEST_TIMEOUT = int(os.getenv("STREAMLIT_TIMEOUT", "30"))

# Page configuration
st.set_page_config(
    page_title="NYC Taxi Duration Predictor",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================
# HEADER
# =============================================
st.title("🚖 NYC Taxi Trip Duration Predictor")
st.markdown("Predict taxi trip duration based on trip details using machine learning")

# =============================================
# SIDEBAR
# =============================================
with st.sidebar:
    st.header("⚙️ Settings")
    page = st.radio(
        "Select Page",
        ["Predict", "Analytics", "About"]
    )

# =============================================
# PREDICTION PAGE
# =============================================
if page == "Predict":
    st.subheader("📍 Enter Trip Details")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trip Information")
        vendor_id = st.selectbox(
            "Vendor ID",
            [1, 2],
            help="Taxi company identifier"
        )
        passenger_count = st.slider(
            "Passenger Count",
            min_value=1,
            max_value=6,
            value=1,
            help="Number of passengers in the trip"
        )
        # Streamlit versions may not have `datetime_input`; use separate
        # date and time inputs and combine them into a datetime object.
        default_dt = datetime.now() - timedelta(hours=1)
        pickup_date = st.date_input(
            "Pickup Date",
            value=default_dt.date(),
            help="Date when trip started"
        )
        pickup_time = st.time_input(
            "Pickup Time",
            value=default_dt.time().replace(microsecond=0),
            help="Time when trip started"
        )
        pickup_datetime = datetime.combine(pickup_date, pickup_time)
    
    with col2:
        st.subheader("Locations (NYC Coordinates)")
        pickup_lat = st.number_input(
            "Pickup Latitude",
            min_value=40.5,
            max_value=40.95,
            value=40.75,
            step=0.01,
            help="Pickup location latitude (40.5-40.95)"
        )
        pickup_lon = st.number_input(
            "Pickup Longitude",
            min_value=-74.3,
            max_value=-73.7,
            value=-73.99,
            step=0.01,
            help="Pickup location longitude (-74.3 to -73.7)"
        )
    
    # Dropoff location in separate section
    st.subheader("📍 Dropoff Location")
    col1, col2 = st.columns(2)
    
    with col1:
        dropoff_lat = st.number_input(
            "Dropoff Latitude",
            min_value=40.5,
            max_value=40.95,
            value=40.76,
            step=0.01,
            help="Dropoff location latitude (40.5-40.95)"
        )
    
    with col2:
        dropoff_lon = st.number_input(
            "Dropoff Longitude",
            min_value=-74.3,
            max_value=-73.7,
            value=-73.98,
            step=0.01,
            help="Dropoff location longitude (-74.3 to -73.7)"
        )
    
    store_flag = st.selectbox(
        "Store & Forward Flag",
        ["N", "Y"],
        index=0,
        help="Whether the trip data was forwarded before being sent"
    )
    
    # Prediction button
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        predict_button = st.button(
            "🚀 Predict Duration",
            use_container_width=True,
            type="primary"
        )
    
    # Make prediction
    if predict_button:
        with st.spinner("Making prediction..."):
            try:
                payload = {
                    "vendor_id": vendor_id,
                    "passenger_count": passenger_count,
                    "pickup_latitude": pickup_lat,
                    "pickup_longitude": pickup_lon,
                    "dropoff_latitude": dropoff_lat,
                    "dropoff_longitude": dropoff_lon,
                    "pickup_datetime": pickup_datetime.isoformat(),
                    "store_and_fwd_flag": store_flag
                }
                
                response = requests.post(
                    f"{API_URL}/api/v1/predict",
                    json=payload,
                    timeout=REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Prediction Successful!")
                    
                    # Display results in columns
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "⏱ Duration (minutes)",
                            f"{result['trip_duration_minutes']:.2f}",
                            help="Predicted trip duration in minutes"
                        )
                    
                    with col2:
                        st.metric(
                            "⏱ Duration (seconds)",
                            f"{result['trip_duration']:.0f}",
                            help="Predicted trip duration in seconds"
                        )
                    
                    with col3:
                        approx_km = (
                            abs(dropoff_lat - pickup_lat) +
                            abs(dropoff_lon - pickup_lon)
                        ) * 111  # Rough conversion
                        st.metric(
                            "📏 Distance",
                            f"~{approx_km:.1f} km",
                            help="Approximate distance"
                        )
                    
                    # Additional info
                    with st.expander("📋 Trip Summary"):
                        summary_df = pd.DataFrame({
                            "Property": [
                                "Vendor ID",
                                "Passengers",
                                "Pickup Time",
                                "Store & Forward"
                            ],
                            "Value": [
                                vendor_id,
                                passenger_count,
                                pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                store_flag
                            ]
                        })
                        st.table(summary_df)
                
                elif response.status_code == 422:
                    st.error("❌ Invalid input data. Please check your inputs.")
                else:
                    st.error(f"❌ Prediction failed with status {response.status_code}")
                    logger.error(f"API error: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error(f"⚠️ Request timeout. Please check if API is running at {API_URL}")
            except requests.exceptions.ConnectionError:
                st.error(f"⚠️ Cannot connect to API at {API_URL}. Is the server running?")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
                logger.error(f"Prediction error: {e}")

# =============================================
# ANALYTICS PAGE
# =============================================
elif page == "Analytics":
    st.subheader("📊 Analytics Dashboard")
    
    if st.button("🔄 Load Analytics", use_container_width=True):
        with st.spinner("Loading analytics..."):
            try:
                response = requests.get(
                    f"{API_URL}/api/v1/analytics",
                    timeout=REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "📊 Total Predictions",
                            data["total_predictions"]
                        )
                    
                    with col2:
                        st.metric(
                            "⏱ Avg Duration (min)",
                            f"{data['avg_duration'] / 60:.2f}"
                        )
                    
                    with col3:
                        st.metric(
                            "📉 Min Duration (min)",
                            f"{data['min_duration'] / 60:.2f}"
                        )
                    
                    with col4:
                        st.metric(
                            "📈 Max Duration (min)",
                            f"{data['max_duration'] / 60:.2f}"
                        )
                    
                    # Daily trend chart
                    if data["daily"]:
                        st.subheader("📈 Daily Predictions Trend")
                        
                        daily_df = pd.DataFrame(data["daily"])
                        if "date" in daily_df.columns:
                            daily_df["date"] = pd.to_datetime(daily_df["date"])
                            daily_df = daily_df.sort_values("date")
                            
                            # Chart
                            st.line_chart(
                                daily_df.set_index("date")[["count"]],
                                use_container_width=True
                            )
                            
                            # Statistics table
                            st.subheader("Daily Statistics")
                            st.dataframe(
                                daily_df[["date", "count", "avg_duration"]].rename(columns={
                                    "date": "Date",
                                    "count": "Predictions",
                                    "avg_duration": "Avg Duration (s)"
                                }),
                                use_container_width=True,
                                hide_index=True
                            )
                    else:
                        st.info("No prediction data available yet.")
                    
                else:
                    st.error("❌ Failed to load analytics")
                    logger.error(f"Analytics error: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error(f"⚠️ Request timeout. API at {API_URL} is not responding.")
            except requests.exceptions.ConnectionError:
                st.error(f"⚠️ Cannot connect to API at {API_URL}.")
            except Exception as e:
                st.error(f"⚠️ Error loading analytics: {str(e)}")
                logger.error(f"Analytics error: {e}")

# =============================================
# ABOUT PAGE
# =============================================
elif page == "About":
    st.subheader("ℹ️ About This Application")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚖 NYC Taxi Trip Duration Prediction
        
        This application predicts the duration of taxi trips in New York City 
        based on real historical data.
        
        **Features:**
        - 🎯 Accurate predictions using LightGBM
        - 🗺️ Full NYC coordinate support
        - 📊 Real-time analytics
        - 🚀 Fast API responses
        
        ### 🧠 Machine Learning
        
        **Model:** LightGBM Regressor  
        **Features:** 30+ engineered features  
        **Training Data:** NYC taxi trip history  
        **Performance:** R² Score > 0.5
        """)
    
    with col2:
        st.markdown("""
        ### 🏗️ Technology Stack
        
        - **Backend:** FastAPI
        - **Frontend:** Streamlit
        - **Database:** SQLite
        - **ML Framework:** Scikit-Learn, LightGBM
        - **Geospatial:** H3 (Uber's hierarchical spatial index)
        
        ### 📝 Input Requirements
        
        - **Vendor ID:** 1 or 2
        - **Passengers:** 1-6
        - **Coordinates:** NYC bounds
        - **Datetime:** Any valid timestamp
        
        ### 🔧 Configuration
        
        API URL: `{}`
        
        """.format(API_URL))
    
    st.divider()
    
    # Health check
    st.subheader("🏥 System Status")
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )
        if response.status_code == 200:
            st.success(f"✅ API is running and healthy")
        else:
            st.warning(f"⚠️ API returned status {response.status_code}")
    except Exception as e:
        st.error(f"❌ Cannot connect to API: {str(e)}")

# Footer
st.divider()
st.markdown(
    "**NYC Taxi Trip Duration Prediction** | Built with ❤️ | "
    "[GitHub](https://github.com/parthsavaliya01) "
)