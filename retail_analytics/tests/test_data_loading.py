import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')))
import pytest
import pandas as pd
from src.data_loading import load_and_validate_purchases, filter_data
from io import StringIO

def test_load_and_validate_purchases():
    test_csv = """CustomerID,ProductID,Category,PurchaseAmount,PurchaseDate
                  C1,P1,Books,10.5,2025-01-01
                  C2,P2,Electronics,99.99,2025-01-02
               """
    df = pd.read_csv(StringIO(test_csv))
    df.to_csv("tests/test_purchases.csv", index=False)

    loaded_df = load_and_validate_purchases("tests/test_purchases.csv")
    assert loaded_df.shape[0] == 2

    print(loaded_df)

def test_filter_data():
    data = {
        "CustomerID": ["C1", "C2", "C3"],
        "ProductID": ["P1", "P2", "P3"],
        "Category": ["Books", "Electronics", "Books"],
        "PurchaseAmount": [10.5, 99.99, 50.0],
        "PurchaseDate": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"])
    }
    df = pd.DataFrame(data)
    # Filter by category
    filtered = filter_data(df, category="Books")
    assert len(filtered) == 2

    print(filtered)

if __name__ == "__main__":
    test_load_and_validate_purchases()
    test_filter_data()
