# src/filters.py

import pandas as pd
import re

def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    category_sanitized = re.sub(r"[^a-zA-Z0-9\s]+", "", category)
    return df[df["Category"] == category_sanitized]

def filter_by_date_range(df: pd.DataFrame, start_date=None, end_date=None) -> pd.DataFrame:
    if start_date:
        df = df[df["PurchaseDate"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["PurchaseDate"] <= pd.to_datetime(end_date)]
    return df
