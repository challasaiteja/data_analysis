import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')))
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from src.logging_utils import get_logger, log_structured

logger = get_logger(__name__)

def create_customer_clusters(df: pd.DataFrame, n_clusters=4):
    """
    Creates customer clusters using K-Means based on aggregated purchase data.
    Uses feature scaling to ensure better clustering results.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing at least 'CustomerID', 'PurchaseAmount', and 'ProductID'.
    n_clusters : int
        Desired number of clusters for K-Means.

    Returns:
    --------
    customer_group : pd.DataFrame
        A DataFrame where each row is a customer,
        with columns for total spending, purchase count, cluster ID, and cluster label.
    """

    # 1. Aggregate Data by Customer
    customer_group = df.groupby("CustomerID").agg({
        "PurchaseAmount": "sum",   # total spending
        "ProductID": "count"      # total purchase count
    }).rename(columns={
        "PurchaseAmount": "TotalSpending",
        "ProductID": "PurchaseCount"
    })
    customer_group = customer_group.reset_index()  # ensure 'CustomerID' is a column

    # 2. Feature Scaling
    features = ["TotalSpending", "PurchaseCount"]
    # If you've added more features, include them here, e.g. "AvgPurchaseValue"
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(customer_group[features])

    # 3. K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(X_scaled)
    customer_group["Cluster"] = cluster_labels

    # 4. Analyze each cluster’s average stats (for labeling or further insights)
    cluster_info = (
        customer_group.groupby("Cluster")
        .agg({
            "TotalSpending": "mean",
            "PurchaseCount": "mean"
        })
        .reset_index()
        .rename(columns={
            "TotalSpending": "AvgSpending",
            "PurchaseCount": "AvgPurchaseCount"
        })
    )

    # 5. Dynamic Label Assignment
    #    Example: Label clusters in ascending order of AvgSpending as:
    #    Low Spenders -> Moderate Spenders -> High Spenders -> Very High Spenders
    
    # Sorting clusters by average spending
    cluster_info_sorted = cluster_info.sort_values("AvgSpending").reset_index(drop=True)
    
    
    labels_map = {
        0: "Low Spenders",
        1: "Moderate Spenders",
        2: "High Spenders",
        3: "Very High Spenders"
    }
    
    # For each sorted cluster, map it to a label
    cluster_id_to_label = {}
    for i, row in cluster_info_sorted.iterrows():
        actual_cluster_id = row["Cluster"]
        # If we have fewer or more than 4 clusters, you can handle that with a fallback or dynamic naming
        label = labels_map[i] if i in labels_map else f"Cluster {i}"
        cluster_id_to_label[actual_cluster_id] = label

    # Apply labels
    customer_group["ClusterLabel"] = customer_group["Cluster"].map(cluster_id_to_label)

    # 6. Log Summary
    #    Include info about each cluster: e.g., how many customers, average spending/frequency
    log_structured(
        logger,
        "info",
        "Customer clustering completed",
        cluster_summary=cluster_info.to_dict(orient="records")
    )

    return customer_group
