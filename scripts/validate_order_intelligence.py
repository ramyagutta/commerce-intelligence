
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "order_intelligence.csv"
)

df = pd.read_csv(DATA_PATH)

print("\n========== FINAL DATASET VALIDATION ==========")

print("Shape:", df.shape)
print("Unique order IDs:", df["order_id"].nunique())
print("Duplicate order IDs:", df["order_id"].duplicated().sum())

print("\nMissing values:")
print(df.isnull().sum()[df.isnull().sum() > 0])

print("\nOrder status distribution:")
print(df["order_status"].value_counts())

print("\nSample records:")
print(df.head(3).to_string(index=False))

print("\nDelivery metrics:")
print(
    df[["delivery_days", "delivery_delay_days"]].describe()
)
