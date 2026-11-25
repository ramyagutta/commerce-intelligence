import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def build_order_intelligence():

    # 1. Load datasets
    orders = pd.read_csv(RAW_DATA_DIR / "olist_orders_dataset.csv")
    customers = pd.read_csv(RAW_DATA_DIR / "olist_customers_dataset.csv")
    items = pd.read_csv(RAW_DATA_DIR / "olist_order_items_dataset.csv")
    payments = pd.read_csv(RAW_DATA_DIR / "olist_order_payments_dataset.csv")
    reviews = pd.read_csv(RAW_DATA_DIR / "olist_order_reviews_dataset.csv")
    products = pd.read_csv(RAW_DATA_DIR / "olist_products_dataset.csv")
    sellers = pd.read_csv(RAW_DATA_DIR / "olist_sellers_dataset.csv")
    categories = pd.read_csv(
        RAW_DATA_DIR / "product_category_name_translation.csv"
    )

    # 2. Aggregate order items
    item_summary = items.groupby("order_id").agg(
        item_count=("order_item_id", "count"),
        total_price=("price", "sum"),
        total_freight=("freight_value", "sum"),
        unique_products=("product_id", "nunique"),
        unique_sellers=("seller_id", "nunique")
    ).reset_index()

    # 3. Aggregate payments
    payment_summary = payments.groupby("order_id").agg(
        total_payment=("payment_value", "sum"),
        payment_count=("payment_sequential", "count"),
        payment_types=("payment_type", "nunique")
    ).reset_index()

    # 4. Aggregate reviews
    review_summary = reviews.groupby("order_id").agg(
        review_score=("review_score", "mean"),
        review_count=("review_id", "nunique")
    ).reset_index()

    # 5. Aggregate product and seller information per order
    item_details = (
        items
        .merge(products, on="product_id", how="left")
        .merge(categories, on="product_category_name", how="left")
        .merge(sellers, on="seller_id", how="left")
    )

    item_details["product_category_name_english"] = (
        item_details["product_category_name_english"]
        .fillna("unknown")
    )

    category_summary = item_details.groupby("order_id").agg(
        product_categories=(
            "product_category_name_english",
            lambda x: " | ".join(sorted(set(x)))
        ),
        seller_cities=("seller_city", lambda x: " | ".join(sorted(set(x.dropna())))),
        seller_states=("seller_state", lambda x: " | ".join(sorted(set(x.dropna()))))
    ).reset_index()

    # 6. Combine datasets at order level
    order_intelligence = (
    orders
    .merge(customers, on="customer_id", how="left", validate="many_to_one")
    .merge(item_summary, on="order_id", how="left", validate="one_to_one")
    .merge(payment_summary, on="order_id", how="left", validate="one_to_one")
    .merge(review_summary, on="order_id", how="left", validate="one_to_one")
    .merge(category_summary, on="order_id", how="left", validate="one_to_one")
    )

    # 7. Convert timestamps
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        order_intelligence[column] = pd.to_datetime(
            order_intelligence[column],
            errors="coerce"
        )

    # 8. Calculate delivery metrics
    order_intelligence["delivery_days"] = (
        order_intelligence["order_delivered_customer_date"]
        - order_intelligence["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    order_intelligence["delivery_delay_days"] = (
        order_intelligence["order_delivered_customer_date"]
        - order_intelligence["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400


    # 9. Add delivery performance classification

    order_intelligence["delivery_performance"] = "not_delivered"

    delivered_mask = (
        order_intelligence["order_status"] == "delivered"
    )

    order_intelligence.loc[
        delivered_mask & (order_intelligence["delivery_delay_days"] > 0),
        "delivery_performance"
    ] = "late"

    order_intelligence.loc[
        delivered_mask & (order_intelligence["delivery_delay_days"] <= 0),
        "delivery_performance"
    ] = "on_time_or_early"

    # 10. Validate the final dataset
    assert order_intelligence["order_id"].is_unique
    assert len(order_intelligence) == len(orders)


    # 11. Save processed data
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = (
        PROCESSED_DATA_DIR / "order_intelligence.csv"
    )

    order_intelligence.to_csv(output_path, index=False)

    print("Order intelligence dataset created successfully!")
    print("Rows:", len(order_intelligence))
    print("Columns:", len(order_intelligence.columns))
    print("Output:", output_path)

    assert order_intelligence["order_id"].is_unique
    assert len(order_intelligence) == len(orders)

if __name__ == "__main__":
    build_order_intelligence()
