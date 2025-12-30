# Scripts Directory

This directory contains machine learning training and evaluation scripts.

## Scripts

| Script                | Description                                       |
| --------------------- | ------------------------------------------------- |
| `data_exploration.py` | Exploratory data analysis on BRFSS2015 dataset    |
| `train_model.py`      | Train Random Forest classifier and save model.pkl |
| `evaluate_model.py`   | Load and evaluate trained model                   |

## Usage

```bash
# Navigate to server directory
cd /Volumes/Projects/repos/diabetes-risk-assessment/server

# Install dependencies
pip install -r requirements.txt

# Run data exploration
python scripts/data_exploration.py

# Train model (generates artifacts/model.pkl)
python scripts/train_model.py

# Evaluate model
python scripts/evaluate_model.py
```

## Output

- `artifacts/model.pkl` - Trained Random Forest classifier with metadata
