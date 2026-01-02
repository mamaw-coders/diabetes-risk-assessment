# Artifacts Directory

This directory contains trained machine learning model artifacts.

## Files

| File        | Size  | Description                                    |
| ----------- | ----- | ---------------------------------------------- |
| `model.pkl` | ~37MB | Trained Random Forest classifier with metadata |

## Model Info

- **Algorithm**: Random Forest Classifier
- **Training Data**: CDC BRFSS 2015 (70,000+ records)
- **Features**: 17 health indicators

## Usage

The model is automatically loaded by the application on startup.
Path can be configured via the `MODEL_PATH` environment variable.

```python
# Default path
MODEL_PATH=artifacts/model.pkl
```
