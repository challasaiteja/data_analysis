import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from logging_utils import get_logger, log_structured

logger = get_logger(__name__)

def analyze_data(df: pd.DataFrame):
    # Top-selling products
    product_sales = df.groupby("ProductID")["PurchaseAmount"].sum().sort_values(ascending=False).head(10)
    log_structured(logger, "info", "Top products", top_products=product_sales.to_dict())

    # Top categories
    category_sales = df.groupby("Category")["PurchaseAmount"].sum().sort_values(ascending=False)
    log_structured(logger, "info", "Category sales", category_sales=category_sales.to_dict())

    # Average spending per customer
    avg_spend = df.groupby("CustomerID")["PurchaseAmount"].sum().mean()
    log_structured(logger, "info", f"Average spending per customer: {avg_spend:.2f}")

    # Visual Insights
    plt.figure(figsize=(10,6))
    sns.barplot(x=product_sales.index, y=product_sales.values)
    plt.title("Top 10 Selling Products by Revenue")
    plt.xlabel("Product ID")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig("data/top_products.png")
    plt.close()

    return {
        "top_products": product_sales,
        "category_sales": category_sales,
        "avg_spend_per_customer": avg_spend
    }
