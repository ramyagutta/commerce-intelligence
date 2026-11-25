import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = Path("data/raw")

print("Project root:", PROJECT_ROOT)
print("Raw data directory:", RAW_DATA_DIR)
print("Does raw data directory exist?", RAW_DATA_DIR.exists())\

csv_files = list(RAW_DATA_DIR.glob("*.csv"))
print("\nCSV files discovered:", len(csv_files))

for file in csv_files:
    print(file.name)

orders_file = RAW_DATA_DIR / "olist_orders_dataset.csv"

orders_df = pd.read_csv(orders_file)

# --------------------------------
# Orders Dataset: Data Quality Audit
# --------------------------------

# 1. Basic dataset information
print("\n========== DATASET SUMMARY ==========")
print("Shape:", orders_df.shape)
print("Memory usage (MB):", round(orders_df.memory_usage(deep=True).sum() / (1024 ** 2), 2))

# 2. Missing values
print("\n========== MISSING VALUES ==========")
missing = orders_df.isnull().sum()
print(missing[missing > 0])

# 3. Duplicate checks
print("\n========== DUPLICATE CHECK ==========")
print("Duplicate rows:", orders_df.duplicated().sum())
print("Duplicate order IDs:", orders_df["order_id"].duplicated().sum())

# 4. Order status distribution
print("\n========== ORDER STATUS ==========")
print(orders_df["order_status"].value_counts())

# 5. Convert timestamp columns
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders_df[column] = pd.to_datetime(orders_df[column], errors="coerce")

# 6. Calculate delivery metrics
orders_df["delivery_days"] = (
    orders_df["order_delivered_customer_date"] -
    orders_df["order_purchase_timestamp"]
).dt.total_seconds() / 86400

orders_df["delivery_delay_days"] = (
    orders_df["order_delivered_customer_date"] -
    orders_df["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# 7. Delivery performance
delivered_orders = orders_df[
    orders_df["order_status"] == "delivered"
]

print("\n========== DELIVERY PERFORMANCE ==========")
print("Delivered orders:", len(delivered_orders))
print("Average delivery days:", round(delivered_orders["delivery_days"].mean(), 2))
print("Average delivery delay (days):", round(delivered_orders["delivery_delay_days"].mean(), 2))
print("Orders delivered late:", (delivered_orders["delivery_delay_days"] > 0).sum())

# ==========================================
# PROFILE ALL OLIST DATASETS
# ==========================================

def profile_dataset(file_path):
    df = pd.read_csv(file_path)

    profile = {
        "dataset": file_path.name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_mb": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2), 2
        )
    }

    return profile


profiles = []

for file in csv_files:
    profiles.append(profile_dataset(file))

profile_df = pd.DataFrame(profiles)

print("\n========== OLIST DATASET PROFILE ==========")
print(profile_df.to_string(index=False))

# ==========================================
# DATASET SCHEMA DISCOVERY
# ==========================================

print("\n========== DATASET SCHEMAS ==========")

for file in csv_files:
    df = pd.read_csv(file, nrows=0)
    print(f"\n{file.name}")
    print(df.columns.tolist())


# ==========================================
# MISSING VALUE DETAILS
# ==========================================

for filename in [
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv"
]:
    df = pd.read_csv(RAW_DATA_DIR / filename)

    print(f"\n========== {filename} ==========")
    print(df.isnull().sum()[df.isnull().sum() > 0])

# ==========================================
# FINAL SCHEMA AND KEY INSPECTION
# ==========================================

datasets_to_inspect = [
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_sellers_dataset.csv"
]

for filename in datasets_to_inspect:

    df = pd.read_csv(RAW_DATA_DIR / filename)

    print(f"\n========== {filename} ==========")

    print("Columns:", df.columns.tolist())

    missing = df.isnull().sum()
    print("Missing values:")
    print(missing[missing > 0])

    print("Rows:", len(df))