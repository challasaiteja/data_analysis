import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')))
import pytest
import pandas as pd
from src.clustering import create_customer_clusters

def test_create_customer_clusters():
    
    data = {
        "CustomerID": ["C1", "C2", "C3", "C4"],
        "ProductID": ["P1", "P1", "P2", "P2"],
        "Category": ["Cat1", "Cat1", "Cat2", "Cat2"],
        "PurchaseAmount": [100, 200, 300, 400],
        "PurchaseDate": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"])
    }
    df = pd.DataFrame(data)
    result = create_customer_clusters(df, n_clusters=2)
    assert "Cluster" in result.columns
    assert "ClusterLabel" in result.columns

    print(result)

if __name__ == "__main__":
    test_create_customer_clusters()
