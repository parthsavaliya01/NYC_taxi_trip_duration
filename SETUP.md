# Setup Guide

This guide explains how to configure the project from scratch on Windows, Linux, or macOS.

## 1. System Requirements

- Operating systems: Windows 10/11, Linux, or macOS
- Python: 3.8 or newer
- Git: latest stable version
- VS Code: recommended but optional
- RAM: 4 GB minimum, 8 GB recommended
- Storage: at least 2 GB free space
- Internet: required only for installing dependencies and cloning the repository

## 2. Software Installation

### Python

Install Python from the official website and ensure that python and pip are available in your terminal.

### Git

Install Git from https://git-scm.com/ and verify it with:

```bash
git --version
```

### VS Code

Visual Studio Code is optional but recommended for editing and running the project locally.

### Docker (optional)

Docker is optional but useful for running the application in containers. Install Docker Desktop or Docker Engine if you want to use the container workflow.

## 3. Clone the Repository

```bash
git clone <your-repository-url>
cd nyc_taxi_app
```

## 4. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux and macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 5. Activate the Environment

If you are using a new terminal session, activate the environment again:

### Windows

```bash
venv\Scripts\activate
```

### Linux and macOS

```bash
source venv/bin/activate
```

## 6. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 7. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Then update the values in .env if needed. The defaults are already suitable for local development.

## 8. Download or Confirm Required Models

The trained model pipeline is downloaded automatically from Hugging Face Hub at runtime. The repository does not require a local model artifact for inference.

Model configuration is controlled through environment variables:

```bash
MODEL_REPO=parthsavaliya001/nyc-taxi-trip-duration-model
MODEL_FILENAME=taxi_full_pipeline.pkl
```

## 9. Database Setup

The project uses SQLite by default. The database file is created automatically when the application starts.

Default location:

```text
data/artifacts/predictions.db
```

If the file is missing, the application will create it on first use.

## 10. Run the Application

### Start the backend

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start the frontend

```bash
streamlit run streamlit_app/app.py
```

### Use the helper scripts

```bash
./start_backend.sh
./start_frontend.sh
```

### Run with Docker Compose

```bash
docker compose up --build
```

## 11. Verify the Installation

You can confirm the setup by checking the following:

- The backend responds at http://localhost:8000/health
- The API docs load at http://localhost:8000/api/docs
- The Streamlit UI opens at http://localhost:8501

Example health check:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "healthy"}
```

## 12. Common Errors

### ModuleNotFoundError

Install the dependencies again:

```bash
pip install -r requirements.txt
```

### Missing environment variables

Ensure that .env exists and contains the variables from .env.example.

### Port already in use

Change the port in .env or stop the process occupying the port.

### Database connection problems

Delete the SQLite file if needed and restart the app:

```bash
rm -f data/artifacts/predictions.db
```

### Model loading errors

The model pipeline is downloaded from Hugging Face Hub. Ensure internet access and valid Hugging Face configuration.

## 13. Updating Dependencies

To update packages in the environment:

```bash
pip install --upgrade -r requirements.txt
```

## 14. Project Maintenance

Keep the environment reproducible by:
- updating dependencies regularly
- keeping the .env file local and private
- backing up the SQLite database if you plan to store predictions long-term

## 15. Uninstallation

To remove the local environment safely:

```bash
rm -rf venv
```

If you used Docker, remove the containers and images as needed.
