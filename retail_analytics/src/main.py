import os
from data_generation import main as generate_data
from data_loading import load_and_validate_purchases, filter_data
from data_analysis import analyze_data
from clustering import create_customer_clusters
from recommendations import build_collaborative_filtering_model, recommend_for_customer, explain_recommendation
from reporting import generate_pdf_report
from logging_utils import get_logger, log_structured

logger = get_logger(__name__)

def run_pipeline():
    # 1. Generate or Load Data
    if not os.path.exists("data/purchases.csv"):
        generate_data()  # only if needed

    # 2. Load & Validate
    df = load_and_validate_purchases("data/purchases.csv")

    # Example filter: last 6 months
    df = filter_data(df, start_date="2024-07-01", end_date="2025-01-01")

    # 3. Analyze Data
    analysis_results = analyze_data(df)

    # 4. Clustering
    cluster_df = create_customer_clusters(df)

    # 5. Recommendation
    algo = build_collaborative_filtering_model(df)
    sample_customer_id = df["CustomerID"].iloc[0]
    recs = recommend_for_customer(algo, sample_customer_id, df)
    explanation = explain_recommendation(sample_customer_id, recs)

    # 6. PDF Report
    recommendations_text = f"Customer {sample_customer_id} => {recs}, Explanation: {explanation}"
    generate_pdf_report(analysis_results, cluster_df, recommendations_text)

if __name__ == "__main__":
    run_pipeline()
