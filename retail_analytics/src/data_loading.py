import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')))
import pandas as pd
import datetime
import re
from src.logging_utils import get_logger, log_structured

logger = get_logger(__name__)

def load_and_validate_purchases(purchases_file: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(purchases_file)
        # Basic Schema Checks
        required_columns = ["CustomerID", "ProductID", "Category", "PurchaseAmount", "PurchaseDate"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Purchases file schema does not match expected format.")

        # Convert dates
        df["PurchaseDate"] = pd.to_datetime(df["PurchaseDate"], errors="coerce")
        df.dropna(subset=["PurchaseDate"], inplace=True)

        # Basic type checks
        df["PurchaseAmount"] = df["PurchaseAmount"].astype(float)

        log_structured(logger, "info", "Loaded and validated purchases data", row_count=df.shape[0])
        return df
    except Exception as e:
        log_structured(logger, "error", f"Error loading purchases file: {e}")
        raise

def filter_data(df: pd.DataFrame, start_date=None, end_date=None, category=None) -> pd.DataFrame:
    filtered_df = df.copy()
    if start_date:
        filtered_df = filtered_df[filtered_df["PurchaseDate"] >= pd.to_datetime(start_date)]
    if end_date:
        filtered_df = filtered_df[filtered_df["PurchaseDate"] <= pd.to_datetime(end_date)]
    if category:
        # Sanitization: allow only alphanumeric/spaces to prevent injection
        category_sanitized = re.sub(r'[^a-zA-Z0-9\s]+', '', category)
        filtered_df = filtered_df[filtered_df["Category"] == category_sanitized]

    log_structured(logger, "info", "Data filtered", 
                   start_date=start_date, end_date=end_date, category=category_sanitized if category else None)
    return filtered_df
