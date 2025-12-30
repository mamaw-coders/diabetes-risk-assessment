"""
Model Evaluation Script

Loads trained model and generates detailed evaluation reports.
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    precision_recall_curve,
    f1_score,
    recall_score,
    precision_score
)


# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DATASET_PATH = DATA_DIR / "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
MODEL_PATH = ARTIFACTS_DIR / "model.pkl"


def load_model():
    """Load trained model from disk."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Run train_model.py first to train the model."
        )
    
    print(f"Loading model from: {MODEL_PATH}")
    model_data = joblib.load(MODEL_PATH)
    
    print(f"Model trained at: {model_data.get('trained_at', 'Unknown')}")
    print(f"Feature order: {model_data['feature_order'][:5]}... (21 features)")
    
    return model_data


def load_test_data(feature_order):
    """Load and prepare test data."""
    print(f"\nLoading data from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    
    # Use same split as training (random_state=42, test_size=0.2)
    from sklearn.model_selection import train_test_split
    
    X = df[feature_order]
    y = df["Diabetes_binary"]
    
    _, X_test, _, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )
    
    print(f"Test set size: {len(X_test):,} samples")
    return X_test, y_test


def evaluate_threshold_impact(model, X_test, y_test):
    """Analyze impact of different probability thresholds."""
    print("\n" + "="*60)
    print("THRESHOLD ANALYSIS")
    print("="*60)
    
    y_proba = model.predict_proba(X_test)[:, 1]
    
    print("\nThreshold | Precision | Recall | F1 Score")
    print("-" * 50)
    
    for threshold in [0.3, 0.4, 0.5, 0.6, 0.7]:
        y_pred = (y_proba >= threshold).astype(int)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        print(f"  {threshold:.1f}    |   {prec:.4f}  |  {rec:.4f} |  {f1:.4f}")


def evaluate_subgroups(model, feature_order):
    """Evaluate model performance on different subgroups."""
    print("\n" + "="*60)
    print("SUBGROUP ANALYSIS")
    print("="*60)
    
    df = pd.read_csv(DATASET_PATH)
    X = df[feature_order]
    y = df["Diabetes_binary"]
    
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]
    
    # By age group
    print("\n--- Performance by Age Group ---")
    age_groups = {
        "Young (18-39)": df["Age"] <= 4,
        "Middle (40-59)": (df["Age"] >= 5) & (df["Age"] <= 8),
        "Senior (60+)": df["Age"] >= 9
    }
    
    print("Age Group    | Accuracy | Recall | ROC-AUC")
    print("-" * 50)
    for label, mask in age_groups.items():
        acc = (y_pred[mask] == y[mask]).mean()
        rec = recall_score(y[mask], y_pred[mask])
        auc = roc_auc_score(y[mask], y_proba[mask])
        print(f"{label:12s} |  {acc:.4f}  | {rec:.4f} |  {auc:.4f}")
    
    # By BMI category
    print("\n--- Performance by BMI Category ---")
    bmi_groups = {
        "Normal (<25)": df["BMI"] < 25,
        "Overweight": (df["BMI"] >= 25) & (df["BMI"] < 30),
        "Obese (>=30)": df["BMI"] >= 30
    }
    
    print("BMI Category | Accuracy | Recall | ROC-AUC")
    print("-" * 50)
    for label, mask in bmi_groups.items():
        acc = (y_pred[mask] == y[mask]).mean()
        rec = recall_score(y[mask], y_pred[mask])
        auc = roc_auc_score(y[mask], y_proba[mask])
        print(f"{label:12s} |  {acc:.4f}  | {rec:.4f} |  {auc:.4f}")


def print_feature_importance(model, feature_order):
    """Print sorted feature importances."""
    print("\n" + "="*60)
    print("FEATURE IMPORTANCE RANKING")
    print("="*60)
    
    importance_df = pd.DataFrame({
        "feature": feature_order,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    
    print("\nRank | Feature                   | Importance")
    print("-" * 50)
    for i, (_, row) in enumerate(importance_df.iterrows(), 1):
        print(f" {i:2d}  | {row['feature']:25s} | {row['importance']:.4f}")


def main():
    """Run evaluation pipeline."""
    print("="*60)
    print("DIABETES RISK MODEL EVALUATION")
    print("="*60)
    
    # Load model
    model_data = load_model()
    model = model_data["model"]
    feature_order = model_data["feature_order"]
    
    # Print training metrics
    print("\n--- Training Metrics (from model file) ---")
    metrics = model_data.get("metrics", {})
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")
    
    # Load test data
    X_test, y_test = load_test_data(feature_order)
    
    # Threshold analysis
    evaluate_threshold_impact(model, X_test, y_test)
    
    # Subgroup analysis
    evaluate_subgroups(model, feature_order)
    
    # Feature importance
    print_feature_importance(model, feature_order)
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
