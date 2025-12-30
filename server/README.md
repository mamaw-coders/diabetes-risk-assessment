# Diabetes Risk Predictor - Flask Server

Flask-based REST API for diabetes risk prediction using machine learning.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py
```

## Architecture

This project uses a **layered architecture**:

```
app/
├── api/          # Presentation Layer (routes, schemas, error handlers)
├── services/     # Service Layer (business logic)
├── models/       # Data Access Layer (ML model loading/inference)
└── utils/        # Cross-cutting concerns (validators, constants)
```

## API Endpoints

| Method | Endpoint   | Description                            |
| ------ | ---------- | -------------------------------------- |
| POST   | `/predict` | Submit health data for risk assessment |
| GET    | `/health`  | Health check endpoint                  |

## Environment Variables

| Variable     | Default               | Description               |
| ------------ | --------------------- | ------------------------- |
| `FLASK_ENV`  | `development`         | Environment mode          |
| `MODEL_PATH` | `artifacts/model.pkl` | Path to ML model artifact |
