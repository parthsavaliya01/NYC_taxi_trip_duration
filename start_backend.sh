#!/bin/bash
# NYC Taxi Trip Duration Prediction - Quick Start Script
# This script starts both the FastAPI backend and Streamlit frontend

set -e

PROJECT_DIR="/home/parth/Desktop/nyc_taxi_app"

echo "=================================================="
echo "🚖 NYC Taxi Trip Duration Prediction"
echo "=================================================="
echo ""
echo "This script will start:"
echo "  1. FastAPI Backend (port 8000)"
echo "  2. Streamlit Frontend (port 8501)"
echo ""
echo "You will need 2 terminal windows open"
echo ""

# Check if venv exists
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create it first:"
    echo "  cd $PROJECT_DIR"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate venv
cd "$PROJECT_DIR"
source venv/bin/activate

echo "✅ Virtual environment activated"
echo ""
echo "=================================================="
echo "Terminal 1: Starting FastAPI Backend..."
echo "=================================================="
echo "Command: python -m uvicorn app.main:app --reload"
echo ""
echo "Press Ctrl+C to stop. Then open another terminal for step 2."
echo ""

# Start FastAPI
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
