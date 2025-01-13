import pandas as pd
from sklearn.cluster import KMeans
from logging_utils import get_logger, log_structured

logger = get_logger(__name__)

def create_customer_clusters(df: pd.DataFrame, n_clusters=4):
    # Prepare features
    customer_group = df.groupby("CustomerID").agg({
        "PurchaseAmount": "sum",  # total spending
        "ProductID": "count"      # purchase frequency
    }).rename(columns={"PurchaseAmount": "TotalSpending", "ProductID": "PurchaseCount"})
    
    # (Optional) one-hot encode categories if you want category preferences included
    # category_counts = df.groupby(["CustomerID", "Category"]).size().unstack(fill_value=0)
    # customer_group = customer_group.join(category_counts)

    # K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    customer_group["Cluster"] = kmeans.fit_predict(customer_group.values)

    # Label clusters (post-hoc interpretation)
    # Example: find average spending in each cluster, etc.
    cluster_info = customer_group.groupby("Cluster").agg({
        "TotalSpending": "mean",
        "PurchaseCount": "mean",
    }).reset_index()

    # A quick labeling logic (example)
    labels = {}
    for _, row in cluster_info.iterrows():
        cluster_id = row["Cluster"]
        if row["TotalSpending"] > 3000:
            labels[cluster_id] = "High Spenders"
        elif row["PurchaseCount"] > 50:
            labels[cluster_id] = "Frequent Buyers"
        else:
            labels[cluster_id] = "Occasional Buyers"

    customer_group["ClusterLabel"] = customer_group["Cluster"].map(labels)

    log_structured(logger, "info", "Customer clustering completed", cluster_summary=cluster_info.to_dict(orient='records'))
    return customer_group
