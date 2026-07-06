#!/bin/bash
# NYC Taxi Trip Duration Prediction - Streamlit Frontend Starter

set -e

PROJECT_DIR="/home/parth/Desktop/nyc_taxi_app"

# Check if venv exists
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "❌ Virtual environment not found!"
    exit 1
fi

# Activate venv
cd "$PROJECT_DIR"
source venv/bin/activate

echo "=================================================="
echo "🌐 Starting Streamlit Frontend..."
echo "=================================================="
echo ""
echo "Streamlit will open in your browser at:"
echo "  Local: http://localhost:8501"
echo ""
echo "Make sure the FastAPI backend is running on port 8000!"
echo ""

# Start Streamlit
streamlit run streamlit_app/app.py
