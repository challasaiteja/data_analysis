import pytest
import pandas as pd
from src.recommendations import build_collaborative_filtering_model, recommend_for_customer

def test_recommend_for_customer():
    data = {
        "CustomerID": ["C1", "C2", "C3", "C1"],
        "ProductID": ["P1", "P2", "P3", "P4"],
        "Category": ["Books", "Electronics", "Toys", "Books"],
        "PurchaseAmount": [10.5, 99.99, 5.0, 20.0],
        "PurchaseDate": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"])
    }
    df = pd.DataFrame(data)
    algo = build_collaborative_filtering_model(df)
    recommendations = recommend_for_customer(algo, "C1", df, top_n=2)
    assert len(recommendations) == 2  # "C1" has purchased P1, P4 => others are P2, P3 => top 2
