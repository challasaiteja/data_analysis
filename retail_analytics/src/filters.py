# src/filters.py

import pandas as pd
import re

def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    Filter the DataFrame by a specified category.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to filter.
    category : str
        The category to filter by.

    Returns
    -------
    pd.DataFrame
        A DataFrame filtered by the specified category.
    """
    # Sanitize the category input to allow only alphanumeric characters and spaces
    category_sanitized = re.sub(r"[^a-zA-Z0-9\s]+", "", category)
    
    # Filter the DataFrame based on the sanitized category
    return df[df["Category"] == category_sanitized]

def filter_by_date_range(df: pd.DataFrame, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    Filter the DataFrame to only include rows where the PurchaseDate is within the
    specified range.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to filter.
    start_date : str
        The earliest date to include in the filter (inclusive).
    end_date : str
        The latest date to include in the filter (inclusive).

    Returns
    -------
    pd.DataFrame
        A DataFrame filtered by the specified date range.
    """
    # If a start date is provided, filter the DataFrame to include only rows
    # with a PurchaseDate greater than or equal to the start date.
    if start_date:
        df = df[df["PurchaseDate"] >= pd.to_datetime(start_date)]
    
    # If an end date is provided, filter the DataFrame to include only rows
    # with a PurchaseDate less than or equal to the end date.
    if end_date:
        df = df[df["PurchaseDate"] <= pd.to_datetime(end_date)]
    
    return df
