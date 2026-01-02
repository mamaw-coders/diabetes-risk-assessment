# GlucoSense - Flask Server

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

Server runs at `http://localhost:5000`

## Architecture

This project uses a **layered architecture**:

```
server/
├── app/
│   ├── api/          # Presentation Layer (routes, schemas, error handlers)
│   ├── services/     # Service Layer (business logic)
│   ├── models/       # Data Access Layer (ML model loading/inference)
│   └── utils/        # Cross-cutting concerns (validators, constants)
├── artifacts/        # Trained model (model.pkl ~37MB)
├── scripts/          # Training & evaluation scripts
└── tests/            # Pytest test suite
```

## API Endpoints

| Method | Endpoint   | Description                            |
| ------ | ---------- | -------------------------------------- |
| POST   | `/predict` | Submit health data for risk assessment |
| GET    | `/health`  | Health check endpoint                  |

## Scripts

| Script                        | Description                       |
| ----------------------------- | --------------------------------- |
| `scripts/train_model.py`      | Train Random Forest on BRFSS data |
| `scripts/evaluate_model.py`   | Evaluate model metrics            |
| `scripts/data_exploration.py` | Dataset analysis                  |

## Environment Variables

| Variable     | Default               | Description               |
| ------------ | --------------------- | ------------------------- |
| `FLASK_ENV`  | `development`         | Environment mode          |
| `MODEL_PATH` | `artifacts/model.pkl` | Path to ML model artifact |

## Testing

```bash
pytest tests/ -v
```
