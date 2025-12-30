"""
Data Exploration Script

Performs exploratory data analysis on the BRFSS2015 diabetes dataset.
Generates statistics, distributions, and correlation analysis.
"""
from pathlib import Path

import pandas as pd

# Paths
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATASET_PATH = DATA_DIR / "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"


def load_data() -> pd.DataFrame:
    """Load the diabetes dataset."""
    print(f"Loading data from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset shape: {df.shape}")
    return df


def explore_basic_stats(df: pd.DataFrame) -> None:
    """Print basic dataset statistics."""
    print("\n" + "="*60)
    print("BASIC STATISTICS")
    print("="*60)
    
    print(f"\nNumber of records: {len(df):,}")
    print(f"Number of features: {len(df.columns)}")
    print(f"\nFeature names:\n{list(df.columns)}")
    
    print("\n--- Data Types ---")
    print(df.dtypes)
    
    print("\n--- Missing Values ---")
    missing = df.isnull().sum()
    print(f"Total missing values: {missing.sum()}")
    if missing.sum() > 0:
        print(missing[missing > 0])


def explore_target_distribution(df: pd.DataFrame) -> None:
    """Analyze target variable distribution."""
    print("\n" + "="*60)
    print("TARGET VARIABLE DISTRIBUTION (Diabetes_binary)")
    print("="*60)
    
    target_counts = df["Diabetes_binary"].value_counts()
    target_pct = df["Diabetes_binary"].value_counts(normalize=True) * 100
    
    print(f"\nClass 0 (No Diabetes): {target_counts[0.0]:,} ({target_pct[0.0]:.1f}%)")
    print(f"Class 1 (Diabetes):    {target_counts[1.0]:,} ({target_pct[1.0]:.1f}%)")
    print(f"\nClass balance ratio: {target_counts[0.0]/target_counts[1.0]:.2f}:1")


def explore_feature_distributions(df: pd.DataFrame) -> None:
    """Analyze feature distributions."""
    print("\n" + "="*60)
    print("FEATURE DISTRIBUTIONS")
    print("="*60)
    
    # Binary features
    binary_features = [
        "HighBP", "HighChol", "CholCheck", "Smoker", "Stroke",
        "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
        "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "DiffWalk", "Sex"
    ]
    
    print("\n--- Binary Features (% with condition) ---")
    for feat in binary_features:
        if feat in df.columns:
            pct = df[feat].mean() * 100
            print(f"{feat:25s}: {pct:5.1f}%")
    
    # Continuous/ordinal features
    print("\n--- Continuous/Ordinal Features ---")
    continuous_features = ["BMI", "GenHlth", "MentHlth", "PhysHlth", "Age", "Education", "Income"]
    for feat in continuous_features:
        if feat in df.columns:
            print(f"\n{feat}:")
            print(f"  Min: {df[feat].min():.1f}, Max: {df[feat].max():.1f}")
            print(f"  Mean: {df[feat].mean():.2f}, Std: {df[feat].std():.2f}")


def explore_correlations(df: pd.DataFrame) -> None:
    """Analyze feature correlations with target."""
    print("\n" + "="*60)
    print("CORRELATIONS WITH TARGET (Diabetes_binary)")
    print("="*60)
    
    correlations = df.corr()["Diabetes_binary"].drop("Diabetes_binary").sort_values(ascending=False)
    
    print("\nTop positive correlations:")
    for feat, corr in correlations.head(10).items():
        print(f"  {feat:25s}: {corr:+.3f}")
    
    print("\nTop negative correlations:")
    for feat, corr in correlations.tail(5).items():
        print(f"  {feat:25s}: {corr:+.3f}")


def explore_diabetes_rates(df: pd.DataFrame) -> None:
    """Analyze diabetes rates by key features."""
    print("\n" + "="*60)
    print("DIABETES RATES BY KEY FEATURES")
    print("="*60)
    
    # By age category
    print("\n--- By Age Category ---")
    age_rates = df.groupby("Age")["Diabetes_binary"].mean() * 100
    for age_cat, rate in age_rates.items():
        age_labels = {
            1: "18-24", 2: "25-29", 3: "30-34", 4: "35-39", 5: "40-44",
            6: "45-49", 7: "50-54", 8: "55-59", 9: "60-64", 10: "65-69",
            11: "70-74", 12: "75-79", 13: "80+"
        }
        label = age_labels.get(int(age_cat), str(age_cat))
        print(f"  {label:10s}: {rate:5.1f}%")
    
    # By BMI category
    print("\n--- By BMI Category ---")
    df["BMI_Category"] = pd.cut(
        df["BMI"],
        bins=[0, 18.5, 25, 30, 100],
        labels=["Underweight", "Normal", "Overweight", "Obese"]
    )
    bmi_rates = df.groupby("BMI_Category", observed=True)["Diabetes_binary"].mean() * 100
    for cat, rate in bmi_rates.items():
        print(f"  {cat:12s}: {rate:5.1f}%")
    
    # By high BP and cholesterol
    print("\n--- By Risk Factors ---")
    print(f"  With High BP:       {df[df['HighBP']==1]['Diabetes_binary'].mean()*100:.1f}%")
    print(f"  Without High BP:    {df[df['HighBP']==0]['Diabetes_binary'].mean()*100:.1f}%")
    print(f"  With High Chol:     {df[df['HighChol']==1]['Diabetes_binary'].mean()*100:.1f}%")
    print(f"  Without High Chol:  {df[df['HighChol']==0]['Diabetes_binary'].mean()*100:.1f}%")


def main():
    """Run all exploration functions."""
    print("="*60)
    print("DIABETES DATASET EXPLORATION")
    print("="*60)
    
    df = load_data()
    explore_basic_stats(df)
    explore_target_distribution(df)
    explore_feature_distributions(df)
    explore_correlations(df)
    explore_diabetes_rates(df)
    
    print("\n" + "="*60)
    print("EXPLORATION COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
