"""
Model Training Script

Trains a Random Forest classifier for diabetes risk prediction.
Generates model.pkl artifact for Flask application.
"""
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_val_score, train_test_split

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DATASET_PATH = DATA_DIR / "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
MODEL_PATH = ARTIFACTS_DIR / "model.pkl"

# Feature order must match constants.py in the application
FEATURE_ORDER = [
    "HighBP",
    "HighChol",
    "CholCheck",
    "BMI",
    "Smoker",
    "Stroke",
    "HeartDiseaseorAttack",
    "PhysActivity",
    "Fruits",
    "Veggies",
    "HvyAlcoholConsump",
    "AnyHealthcare",
    "NoDocbcCost",
    "GenHlth",
    "MentHlth",
    "PhysHlth",
    "DiffWalk",
    "Sex",
    "Age",
    "Education",
    "Income",
]


def load_and_prepare_data():
    """Load dataset and prepare features/target."""
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset shape: {df.shape}")
    
    # Validate feature order
    for feat in FEATURE_ORDER:
        if feat not in df.columns:
            raise ValueError(f"Feature '{feat}' not found in dataset!")
    
    # Prepare features and target
    X = df[FEATURE_ORDER]
    y = df["Diabetes_binary"]
    
    print(f"Features shape: {X.shape}")
    print(f"Target distribution: {y.value_counts().to_dict()}")
    
    return X, y


def train_model(X_train, y_train):
    """Train Random Forest classifier."""
    print("\nTraining Random Forest classifier...")
    
    # Model hyperparameters
    # Using balanced class_weight to handle any residual imbalance
    # Limiting max_depth for faster inference and to prevent overfitting
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    
    model.fit(X_train, y_train)
    print("Training complete!")
    
    return model


def evaluate_model(model, X_train, y_train, X_test, y_test):
    """Evaluate model performance."""
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    
    # Cross-validation on training set
    print("\n--- Cross-Validation (5-fold) ---")
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="recall")
    print(f"Recall scores: {cv_scores}")
    print(f"Mean CV Recall: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
    
    # Test set predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    print("\n--- Test Set Metrics ---")
    print(f"Accuracy:  {(y_pred == y_test).mean():.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_test, y_proba):.4f}")
    
    # Classification report
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred, target_names=["No Diabetes", "Diabetes"]))
    
    # Confusion matrix
    print("\n--- Confusion Matrix ---")
    cm = confusion_matrix(y_test, y_pred)
    print("                 Predicted")
    print("                 No    Yes")
    print(f"Actual No  {cm[0][0]:6d} {cm[0][1]:6d}")
    print(f"Actual Yes {cm[1][0]:6d} {cm[1][1]:6d}")
    
    # Feature importance
    print("\n--- Top 10 Feature Importances ---")
    importance_df = pd.DataFrame({
        "feature": FEATURE_ORDER,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    
    for _, row in importance_df.head(10).iterrows():
        print(f"  {row['feature']:25s}: {row['importance']:.4f}")
    
    return {
        "cv_recall_mean": cv_scores.mean(),
        "cv_recall_std": cv_scores.std(),
        "test_accuracy": (y_pred == y_test).mean(),
        "test_precision": precision_score(y_test, y_pred),
        "test_recall": recall_score(y_test, y_pred),
        "test_f1": f1_score(y_test, y_pred),
        "test_roc_auc": roc_auc_score(y_test, y_proba)
    }


def save_model(model, metrics):
    """Save trained model to disk."""
    print("\n" + "="*60)
    print("SAVING MODEL")
    print("="*60)
    
    # Ensure artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save model with metadata
    model_data = {
        "model": model,
        "feature_order": FEATURE_ORDER,
        "metrics": metrics,
        "trained_at": datetime.now().isoformat(),
        "sklearn_version": pd.__version__
    }
    
    joblib.dump(model_data, MODEL_PATH)
    
    # Verify file was created
    file_size = MODEL_PATH.stat().st_size / (1024 * 1024)  # MB
    print(f"Model saved to: {MODEL_PATH}")
    print(f"File size: {file_size:.2f} MB")


def main():
    """Main training pipeline."""
    print("="*60)
    print("DIABETES RISK PREDICTION MODEL TRAINING")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    X, y = load_and_prepare_data()
    
    # Split data
    print("\nSplitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )
    print(f"Training set: {len(X_train):,} samples")
    print(f"Test set: {len(X_test):,} samples")
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_model(model, X_train, y_train, X_test, y_test)
    
    # Validate PRD requirements
    print("\n" + "="*60)
    print("PRD REQUIREMENTS VALIDATION")
    print("="*60)
    
    recall_threshold = 0.70
    roc_auc_threshold = 0.75
    
    recall_pass = metrics["test_recall"] >= recall_threshold
    roc_auc_pass = metrics["test_roc_auc"] >= roc_auc_threshold
    
    print(f"Recall >= {recall_threshold}: {'✓ PASS' if recall_pass else '✗ FAIL'} ({metrics['test_recall']:.4f})")
    print(f"ROC-AUC >= {roc_auc_threshold}: {'✓ PASS' if roc_auc_pass else '✗ FAIL'} ({metrics['test_roc_auc']:.4f})")
    
    # Save model
    save_model(model, metrics)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    return model, metrics


if __name__ == "__main__":
    main()
